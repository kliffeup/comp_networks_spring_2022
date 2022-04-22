# pip install more_itertools, if needed
from more_itertools import windowed


def get_checksum(byte_array: bytes) -> bytes:
    sum = 0
    for (byte1, byte2) in windowed(byte_array, n=2, step=2):
        sum += byte1 * 256 + byte2
        sum %= 65536

    return (65535 - sum).to_bytes(length=2, byteorder='big')


def is_valid_checksum(byte_array: bytes, checksum: bytes) -> bool:
    sum = int.from_bytes(checksum, byteorder='big')
    for (byte1, byte2) in windowed(byte_array, n=2, step=2):
        sum += byte1 * 256 + byte2
        sum %= 65536

    return 65535 == sum


# example from lecture
# input byte array:
# 0110011001100000 -> b'\x66\x60'
# 0101010101010101 -> b'\x55\x55'
# 1000111100001100 -> b'\x8f\x0c'
# correct checksum:
# 1011010100111110 -> b'\xb5\x3e'

example1 = bytes(b'\x66\x60\x55\x55\x8f\x0c')
assert get_checksum(example1) == b'\xb5\x3e'
assert is_valid_checksum(example1, b'\x16\x42') == False
assert is_valid_checksum(example1, b'\xb5\x3e') == True

# input byte array:
# 1101000100001101 -> b'\xd1\x0d'
# 0111001010110010 -> b'\x72\xb2'
# 1111000001001101 -> b'\xf0\x4d'
# 1001101010010001 -> b'\x9a\x91'
# correct checksum:
# 0011000101100010 -> b'\x31\x62'

example2 = bytes(b'\xd1\x0d\x72\xb2\xf0\x4d\x9a\x91')
assert get_checksum(example2) == b'\x31\x62'
assert is_valid_checksum(example2, b'\x31\x61') == False
assert is_valid_checksum(example2, b'\x31\x62') == True

# input byte array
# 0111011010110101 -> b'\x76\xb5'
# correct checksum:
# 1000100101001010 -> b'\x89\x4a'

example3 = b'\x76\xb5'
assert get_checksum(example3) == b'\x89\x4a'
assert is_valid_checksum(example3, b'\x4a\x89') == False
assert is_valid_checksum(example3, b'\x89\x4a') == True

# input byte array
# 0000000000000000 -> b'\x00\x00'
# correct checksum:
# 1111111111111111 -> b'\xff\xff'

dummy_example = b'\x00\x00'
assert get_checksum(dummy_example) == b'\xff\xff'
assert is_valid_checksum(dummy_example, b'\xef\xff') == False
assert is_valid_checksum(dummy_example, b'\xff\xff') == True
