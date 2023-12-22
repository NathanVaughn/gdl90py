from functools import cache

from bitstring import BitArray

from gdl90py.exceptions import InvalidCRC, MissingFlagBytes
from gdl90py.utils.bitarray import lsb_bytes

FLAG_BYTE = 0x7E
CONTROL_ESCAPE_BYTE = 0x7D
ESCAPE_XOR_BYTE = 0x20
MASK_16_BIT = 0xFFFF
FOREFLIGHT_MESSAGE_ID = 0x65


@cache
def crc_table() -> list[int]:
    """
    Builds the CRC table.
    """
    table = []
    for i in range(256):
        crc = (i << 8) & MASK_16_BIT
        for _ in range(8):
            crc = ((crc << 1) & MASK_16_BIT) ^ (0x1021 if crc & 0x8000 else 0)
        table.append(crc)

    return table


def compute_crc(data: bytes) -> bytes:
    """
    Computes the CRC for the given input and returns 2 bytes
    """
    crc = 0
    for c in data:
        m = crc << 8 & MASK_16_BIT
        crc = crc_table()[(crc >> 8)] ^ m ^ c

    return crc.to_bytes(length=2, byteorder="little")


def check_crc(data: bytes, crc: bytes) -> bool:
    """
    Checks if CRC is valid.
    """
    return compute_crc(data) == crc


def escape(data: bytes) -> bytearray:
    """
    Properly escape the byte array
    """
    new_data = bytearray()
    bytes_to_escape = {FLAG_BYTE, CONTROL_ESCAPE_BYTE}

    for item in data:
        if item in bytes_to_escape:
            new_data.append(CONTROL_ESCAPE_BYTE)
            new_data.append(item ^ ESCAPE_XOR_BYTE)
        else:
            new_data.append(item)

    return new_data


def unescape(data: bytes) -> bytearray:
    """
    Unescape the byte array
    """
    escaped_data = bytearray()

    while CONTROL_ESCAPE_BYTE in data:
        escape_index = data.index(CONTROL_ESCAPE_BYTE)
        # Everything up to the escape character
        escaped_data.extend(data[:escape_index])

        # XOR with 0x20 to get the escaped value
        escaped_value = data[escape_index + 1] ^ ESCAPE_XOR_BYTE
        # Appending the escaped value
        escaped_data.append(escaped_value)

        # Remove prefix bytes, escape, and escaped value
        data = data[escape_index + 2 :]

    # Append the remaining characters after processing escapes
    escaped_data.extend(data)
    return escaped_data


def build(message_ids: tuple[int, ...], data: BitArray, outgoing_lsb: bool) -> bytes:
    """
    Build a message by adding ID(s), CRC, and flag bytes.
    """
    message_id_bytes = b""
    for message_id in message_ids:
        message_id_bytes += message_id.to_bytes()

    # add the message ID to the front
    message_id_data = message_id_bytes + data.tobytes()

    # add the CRC
    message_id_data_crc = message_id_data + compute_crc(message_id_data)

    # escape
    message_id_data_crc_escaped = escape(message_id_data_crc)

    # add flag bytes
    message_id_data_crc_escaped.insert(0, FLAG_BYTE)
    message_id_data_crc_escaped.append(FLAG_BYTE)

    # flip bit order
    if outgoing_lsb:
        message_id_data_crc_escaped = lsb_bytes(message_id_data_crc_escaped)
    else:
        message_id_data_crc_escaped = bytes(message_id_data_crc_escaped)

    return message_id_data_crc_escaped


def deconstruct(
    data: bytes | bytearray, incoming_msb: bool
) -> tuple[tuple[int, ...], BitArray]:
    """
    Deconstruct a message. Checks the CRC and returns the message ID(s)
    and the message data seperately.
    """

    if data[0] != FLAG_BYTE and data[-1] != FLAG_BYTE:
        raise MissingFlagBytes("Data is missing flag bytes")

    # Remove flag bytes
    message_without_flags = data[1:-1]

    # Flip bit order
    if not incoming_msb:
        message_without_flags = lsb_bytes(message_without_flags)

    # Unescape the data
    unescaped_message = unescape(message_without_flags)

    # Extract the data and CRC
    received_crc = unescaped_message[-2:]
    message_id_data = unescaped_message[:-2]

    # check the CRC
    if not check_crc(message_id_data, received_crc):
        raise InvalidCRC("Invalid CRC")

    # Extract message ID and data
    message_id = message_id_data[0]

    # ForeFlight messages have a sub ID
    if message_id == FOREFLIGHT_MESSAGE_ID:
        message_ids = (message_id, message_id_data[1])
        message_data = message_id_data[2:]
    else:
        message_ids = (message_id,)
        message_data = message_id_data[1:]

    return message_ids, BitArray(message_data)
