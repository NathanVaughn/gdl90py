import textwrap

from bitstring import BitArray


def pop_bits(bitarray: BitArray, bits: int) -> BitArray:
    """
    Returns the first X elements of the bitarray. Removes those elements
    from the given bitarray in-place.
    """
    value = bitarray[:bits]
    del bitarray[:bits]
    return value


def lsb(bitarray: BitArray) -> BitArray:
    """
    Flips the order of the bits in each byte.
    """
    new = BitArray()
    for byte in bitarray.cut(8):
        new.append(byte[::-1])
    return new


def lsb_bytes(bytes_: bytes | bytearray) -> bytes:
    """
    Flips the order of the bits in each byte.
    """
    return lsb(BitArray(bytes_)).bytes


def lsb_bytearray(bytearray_: bytearray) -> bytearray:
    """
    Flips the order of the bits in each byte.
    """
    return bytearray(lsb(BitArray(bytearray_)).bytes)


def lsb_int(int_: int, length: int = 8) -> int:
    """
    Flips the order of the bits in each byte.
    """
    return lsb(BitArray(uint=int_, length=length)).uint


def format_hex(data: BitArray | bytes | bytearray) -> str:
    """
    Print a bitarray as seperate hexadecimal pairs.
    """
    if isinstance(data, BitArray):
        return " ".join(f"0x{h}" for h in textwrap.wrap(data.hex, 2))
    else:
        return " ".join("0x{:02x}".format(b) for b in data)
