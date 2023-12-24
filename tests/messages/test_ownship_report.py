from gdl90py.messages.ownship_report import OwnshipReportMessage


def test_ownship_report():
    assert OwnshipReportMessage.MESSAGE_IDS == (10,)
