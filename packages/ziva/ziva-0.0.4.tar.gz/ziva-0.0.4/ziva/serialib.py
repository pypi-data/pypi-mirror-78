from time import sleep
from serial.tools import list_ports
import serial
import logging


logger = logging.getLogger(__name__)


def comports():
    """Lists available comports"""

    available_ports = []
    ports = list_ports.comports()
    for port in ports:
        available_ports.append(str(port))
    return available_ports


def serial_ports():
    """Filter serial ports from all comports and strip away description of port"""

    ports = comports()
    ser_ports = list(filter(lambda x: 'Serial Port' in x, ports))
    ser_ports = [i.split(' ')[0] for i in ser_ports]
    return ser_ports


def autodetermine_port():
    """Auto select first serial port"""

    ser_ports = serial_ports()
    if ser_ports:
        return serial_ports()[0]


class SerialComm(object):
    def __init__(self):
        self.port = None
        self.baudrate = 38400
        self.timeout = 0.1
        self.n_retry = 3
        self.ser = None

    def open(self):
        """Connect to serial port"""

        if self.port == None:
            raise Exception('You have to set a serial port')

        if self.ser:
            self.close()

        for i in range(self.n_retry):
            try:
                self.ser = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=self.timeout
                )
                self.ser.flushInput()
                logger.debug(f"Serial port opened:{self.port}, baud:{self.baudrate}")
                logger.debug(f"Serial port flushed")
                break
            except Exception as e:
                logger.error(f"Failed to open serial port:{self.port}, error:{e}")
                sleep(1)

    def close(self):
        """Close serial port"""

        self.ser.close()
        self.ser = None

    def reopen_port(self):
        """Reopen serial port. This is sometimes necessary if it stops working."""

        self.open()

    def write(self, data: bytes = None):
        """Write bytes to serial port"""

        if self.ser == None:
            self.open()

        if not data:
            raise ValueError('No bytes to send')

        logger.debug(f"Data sent: {data}")
        if data:
            self.ser.write(data)

    def readline(self):
        line = self.ser.readline()
        return line

    def read(self, last_char=b'\x83'):
        """Read from serial 1 byte at a time. Stop when last_char is received."""

        frame = b""
        while True:
            byte = self.ser.read(1)
            if byte:
                frame += byte
                if byte == last_char:
                    break
            else:
                break
        logger.debug(f"Data received: {frame}")
        return frame
