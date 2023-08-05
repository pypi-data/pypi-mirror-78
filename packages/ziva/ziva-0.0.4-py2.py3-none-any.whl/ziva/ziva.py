import json
import logging
from time import sleep, time
from datetime import datetime

from .comm_package import validate_data, define_package, data_to_parsed_string
from .serialib import SerialComm, autodetermine_port
from .const import *
from .exceptions import NoAnswer, InvalidAnswer, InvalidCommand, CRCError

logger = logging.getLogger(__name__)


class Ziva(SerialComm):
    def __init__(self):
        super().__init__()
        self.port = None
        self.baudrate = 38400
        self.timeout = 0.1
        self.package_counter = 0
        self.rv_units = []
        self.rv_names = []
        self.real_values = []
        self.info_params = {}
        self.write_commands = []
        self.memory_status = None
        self.latest_data = {}

    def set_port(self, port: str = None, baudrate: int = 38400, timeout: float = 0.5):
        self.port = port if port else autodetermine_port()
        self.baudrate = baudrate
        self.timeout = timeout
        self.open()

    def get_latest_data(self) -> dict:
        """ Get latest data from device.
        Latest data are info_params and real values.
        Update parameters if they were changed

        :return: dictionary with latest data
        """
        real_values_cmds = [RV_MASK, RV_UNITS, RV_NAMES]
        info_params_cmds = [IDENT_A, IDENT_B, IDENT_C, ID_0]

        # Update any info params that had been changed
        for cmd in self.write_commands:
            if cmd in info_params_cmds:
                data = self.read_variable(name=cmd)['data']
                self.info_params[cmd.lower()] = data

        if any(item in self.write_commands for item in real_values_cmds):
            self.real_values = []

        self.read_real_values()
        self.latest_data = {
            'real_values': self.real_values,
            'info_params': self.info_params,
            'memory_status': self.memory_status
        }
        return self.latest_data

    def __increment_counter(self):
        if self.package_counter == 255:
            self.package_counter = 0
        else:
            self.package_counter += 1

    def set_device(self, recv_address: int, rf: bool = True):
        self.recv_address = recv_address
        self.rf = rf

    def define_package(self, app_cmd:str = None, var_name:str = None, var_val:str = None):
        package = define_package(
            recv_addr=self.recv_address,
            app_cmd=app_cmd,
            var_name=var_name,
            var_val=var_val,
            counter=self.package_counter,
            rf=self.rf
        )
        return package

    def send_receive(self, app_cmd: str, var_name: str = None, var_val: str = None, retry_limit: int = None,
                     timeout:float = 1, stream_channel: bool = False, parse: bool = True) -> dict:
        '''Sent package and receive answer.'''

        if self.ser != None:
            self.ser.timeout = timeout

        for error_count in range(20):
            try:
                self.__increment_counter()
                package = self.define_package(
                    app_cmd=app_cmd,
                    var_name=var_name,
                    var_val=var_val,
                )
                self.write(data=package)
                data = self.read(last_char=END_MARKER_BYTES)
                data = validate_data(data, stream_channel=stream_channel)
                if stream_channel:
                    # data['data'] = data_decompress(data=data['data'])
                    data['data'] = ''.join(chr(i) for i in data['data'])
                else:
                    data['data'] = data_to_parsed_string(data=data['data'])
            except (NoAnswer, InvalidAnswer, CRCError, InvalidCommand, Exception) as e:
                if retry_limit:
                    if retry_limit == error_count:
                        raise
                else:
                    if type(e).__name__ == NoAnswer.__name__:
                        retry = RETRY_NO_ANSWER
                    elif type(e).__name__ == InvalidAnswer.__name__:
                        retry = RETRY_INVALID_ANSWER
                    elif type(e).__name__ == CRCError.__name__:
                        retry = RETRY_CRC_ERROR
                    elif type(e).__name__ == InvalidCommand.__name__:
                        retry = RETRY_INVALID_COMMAND
                    else:
                        retry = 2
                    if error_count == retry:
                        raise
            else:
                return data

    def read_variable(self, name) -> dict:
        return self.send_receive(app_cmd=VALUE_READ, var_name=name)

    def write_variable(self, name, value) -> dict:
        """Write variable.
        """

        self.write_commands.append(name)
        return self.send_receive(app_cmd=VALUE_WRITE, var_name=name, var_val=value)

    def read_real_values(self) -> list:
        """ Read real values from device
        Possible output from real values variable:
        - '7005968.000','0.00','-83.94'
        - '29/08/2020 18:39:47','25.740','3.42'
        """

        # If real values were not previously read, read other params also (units,mask,names)
        if not self.real_values:
            self.rv_units = []
            self.rv_names = []
            rv_mask = self.read_variable(name=RV_MASK)['data']
            rv_units = self.read_variable(name=RV_UNITS)['data'].split(';')
            rv_names = self.read_variable(name=RV_NAMES)['data'].split(';')
            if rv_mask and rv_units and rv_names:
                for i, mask in enumerate(rv_mask):
                    if bool(int(mask)):
                        self.rv_units.append(rv_units[i])
                        self.rv_names.append(rv_names[i])

        # Read real values
        real_values = self.read_variable(name=REAL_VALUES)['data']
        self.real_values = []

        # First real value can be timestamp
        try:
            datetime.strptime(real_values[0], "%d/%m/%Y %H:%M:%S")
            self.real_values.append({'channel':'Timestamp', 'value':real_values[0], 'unit':None})
            real_values.pop(0)
        except ValueError:
            pass

        for i, val in enumerate(real_values):
            meas = {
                'channel': self.rv_names[i],
                'value': val,
                'unit': self.rv_units[i]
            }
            self.real_values.append(meas)
        return self.real_values

    def read_params(self):
        data = []
        error_count = 0
        max_error_count = 5
        for i in range(500):
            var_name = f'PAR[{i}]'
            try:
                params = self.send_receive(app_cmd=VALUE_READ, var_name=var_name)['data']
                if params == 'End':
                    break
                elif len(params) > 0:
                    params_dict = {}
                    for par in params:
                        if '=' in par:
                            params_dict[par.split('=')[0].lower()] = par.split('=')[1]
                        else:
                            params_dict[par.lower()] = True
                    value = self.read_variable(name=params_dict['name'])['data']
                    params_dict['value'] = value
                    data.append(params_dict)
            except Exception as e:
                logger.warning(f'Cant read param {var_name}, e:{e}')
                error_count += 1
                if error_count == max_error_count:
                    break
                else:
                    continue
        logger.info(f'Settings parameters read, count:{len(data)}')
        return data

    def get_memory_status(self):
        data = self.send_receive(app_cmd=MEMORY_STATUS)['data']
        size, free, used = int(data[0]), int(data[1]), int(data[2])
        self.memory_status = {'size':size, 'free': free, 'used':used, 'used_percentage':round(used / size * 100, 1)}
        return self.memory_status

    def read_memory_data(self, filepath: str = 'data.jda'):
        """Read memory from device and save data to filepath"""

        self.send_receive(app_cmd=OPEN_MEMORY_DIR)
        data_out = ''
        while True:
            data = self.send_receive(app_cmd=MEMORY_START_READING, stream_channel=True, timeout=2)
            data_out += data['data']
            if data['status'] == 'OT':
                break
        if data_out:
            with open(filepath, 'w', encoding='latin1') as f:
                f.write(data_out)

    def save_params(self, filepath:str = 'settings.txt'):
        """Save params to filepath"""
        data = self.read_params()
        with open(filepath, 'w') as f:
            f.write(json.dumps(data))

    def load_params(self, filepath: str):
        with open(filepath) as f:
            data = json.load(f)

    def read_info_variables(self):
        """Get info parameters"""
        data = {
            'ident_a':IDENT_A,
            'ident_b':IDENT_B,
            'ident_c':IDENT_C,
            'id_0': ID_0,
        }
        for key, val in data.items():
            try:
                var = self.read_variable(name=val)['data']
                data[key] = var
            except Exception as e:
                continue
        self.info_params = data
        return self.info_params

    def reset_rf_device(self):
        pass

    def reset_cpu(self):
        return self.send_receive(app_cmd=RESET_CPU)

    def goto_sleep(self):
        return self.send_receive(app_cmd=DEVICE_SLEEP)

    def start_wake_up_routine(self):
        start = time()
        app_cmd = f"{WAKE_UP_DEVICE}{self.recv_address},{WAKE_UP_TIME_TOTAL}"
        try:
            self.send_receive(app_cmd=app_cmd, retry_limit=3, timeout=0.1)
            sleep(WAKE_UP_TIME_TOTAL)
        except NoAnswer:
            raise NoAnswer('USB router is busy or not working properly')
        wake_time = round(time() - start, 1)
        logger.info(f'Device woke up in {wake_time} seconds')

    def go_online(self) -> dict:
        """
        Go online. If remote device is RF start wake_up procedure.
        :return: dict of info parameters
        """
        if self.rf:
            self.start_wake_up_routine()

        self.read_info_variables()

        if self.rf:
            self.get_memory_status()

        return self.get_latest_data()

