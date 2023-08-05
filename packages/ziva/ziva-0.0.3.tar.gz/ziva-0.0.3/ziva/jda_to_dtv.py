from binascii import hexlify, unhexlify

t = """gÚ´RZ@¶'gÚð\x00RYï¶'gÛ,RZR¶'gÛhRZú¶'gÛ¤RZ~¶'gÛàRZ\x96¶'gÜ\x1cRYü¶'gÜXRZk¶'gÜ\x94RZx¶'gÜÐRZ\x96¶'gÝ\x0cRZÎ¶'gÝHR[1¶'gÝ\x844R[i¶'gÝÀR[\x00¶"""
print (unhexlify(t))


# with open('data.jda', 'w', encoding='latin1') as f:
#     f.write(t)

def jda_to_dtv(filepath) -> str:
    with open(filepath, 'r') as f:
        lines = f.readlines()

    file_out = ''
    return file_out
