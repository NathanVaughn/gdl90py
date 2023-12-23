from gdl90py.messages.long_uat_report import LongUATReportMessage


def test_long_uat_report():
    assert LongUATReportMessage.MESSAGE_IDS == (31,)
    assert LongUATReportMessage.UPLINK_PAYLOAD_BITS == 34 * 8
