import gdl90py.utils.gdl90
from gdl90py.exceptions import UnkownMessageID
from gdl90py.messages._base_message import BaseMessage
from gdl90py.messages.basic_uat_report import BasicUATReportMessage
from gdl90py.messages.foreflight_ahrs import ForeFlightAHRSMessage
from gdl90py.messages.foreflight_id import ForeFlightIDMessage
from gdl90py.messages.heartbeat import HeartbeatMessage
from gdl90py.messages.height_above_terrain import HeightAboveTerrainMessage
from gdl90py.messages.initialization import InitializationMessage
from gdl90py.messages.long_uat_report import LongUATReportMessage
from gdl90py.messages.ownship_geometric_altitude import OwnshipGeometricAltitudeMessage
from gdl90py.messages.ownship_report import OwnshipReportMessage
from gdl90py.messages.traffic_report import TrafficReportMessage
from gdl90py.messages.uplink_data import UplinkDataMessage

KNOWN_MESSAGE_TYPES: dict[tuple[int, ...], BaseMessage] = {
    msg.MESSAGE_IDS: msg
    for msg in [
        OwnshipGeometricAltitudeMessage,
        InitializationMessage,
        HeartbeatMessage,
        ForeFlightIDMessage,
        ForeFlightAHRSMessage,
        UplinkDataMessage,
        BasicUATReportMessage,
        LongUATReportMessage,
        HeightAboveTerrainMessage,
        OwnshipReportMessage,
        TrafficReportMessage,
    ]
}


def parse_message(
    data: bytes, incoming_msb: bool = True, ignore_unknown: bool = False
) -> BaseMessage | None:
    """
    Given a single message, parse and return a data class.
    """
    message_ids, message_data = gdl90py.utils.gdl90.deconstruct(data, incoming_msb)
    if message_ids not in KNOWN_MESSAGE_TYPES:
        # skip if asked to ignore
        if ignore_unknown:
            return None

        raise UnkownMessageID(f"Unknown message ID(s) {message_ids}.")

    return KNOWN_MESSAGE_TYPES[message_ids].deserialize(message_data)


def parse_messages(
    data: bytes, incoming_msb: bool = True, ignore_unknown: bool = False
) -> list[BaseMessage]:
    """
    Given multiple possible messages, parse and return a list of data classes.
    `incoming_msb` should be set to True if the bytes provided have the Most
    Signficiant Bit first.
    """
    flag_byte_count = data.count(gdl90py.utils.gdl90.FLAG_BYTE)
    message_count = int(flag_byte_count / 2)

    output: list[BaseMessage] = []

    for _ in range(message_count):
        # find the next flag byte. offset by one to skip the first one
        message_end_index = data.index(gdl90py.utils.gdl90.FLAG_BYTE, 1)
        # parse the message
        msg = parse_message(data[: message_end_index + 1], incoming_msb, ignore_unknown)
        if msg is not None:
            output.append(msg)
        # slice the parsed data off
        data = data[message_end_index + 1 :]

    return output
