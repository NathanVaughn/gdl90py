from gdl90py.messages.basic_uat_report import BasicUATReportMessage


def test_basic_uat_report():
    assert BasicUATReportMessage.MESSAGE_IDS == (30,)
    assert BasicUATReportMessage.UPLINK_PAYLOAD_BITS == 18 * 8
