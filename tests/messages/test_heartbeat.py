import datetime

from gdl90py.messages.heartbeat import HeartbeatMessage


def test_message_count_serialize():
    hb = HeartbeatMessage(
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        datetime.datetime.now().time(),
        4,
        567,
    )
    data = hb.serialize(outgoing_lsb=False)
    assert data[6] == 0x22
    assert data[7] == 0x37
