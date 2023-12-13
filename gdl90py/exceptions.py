class UnkownMessageID(Exception):
    pass


class DataTooLong(Exception):
    pass


class InvalidCRC(Exception):
    pass


class MissingFlagBytes(Exception):
    pass


class InvalidCallsign(Exception):
    pass


class UnexpectedNegative(Exception):
    pass


class UplinkDataWrongSize(Exception):
    pass


class BadIntegerSize(Exception):
    pass
