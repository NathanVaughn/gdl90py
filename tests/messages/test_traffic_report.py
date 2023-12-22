import pytest

from gdl90py.enums import (
    Accuracy,
    AddressType,
    EmergencyPriorityCode,
    EmitterCategory,
    Integrity,
    TrackType,
)
from gdl90py.messages.traffic_report import TrafficReportMessage


def test_traffic_report_serialize():
    tr = TrafficReportMessage(
        traffic_alert=False,
        address_type=AddressType.ads_b_icao,
        address=int("52642511", 8),
        latitude=44.90708,
        longitude=-122.99488,
        pressure_altitude=5000,
        track_type=TrackType.true_track_angle,
        report_extrapolated=False,
        airborne=True,
        integrity=Integrity.less_than_25_m_hpl_and_37_5_m_vpl,
        accuracy=Accuracy.less_than_30_m_hfom_and_45_m_vfom,
        horizontal_velocity=123,
        vertical_velocity=64,
        track=45,
        emitter_category=EmitterCategory.light,
        callsign="N825V",
        emergency_priority_code=EmergencyPriorityCode.no_emergency,
    )
    assert (
        tr.serialize(outgoing_lsb=False)
        == b"\x7E\x14\x00\xAB\x45\x49\x1F\xEF\x15\xA8\x89\x78\x0F\x09\xA9\x07\xB0\x01\x20\x01\x4E\x38\x32\x35\x56\x20\x20\x20\x00\x57\xD6\x7e"
    )


def test_traffic_report_deserialize():
    tr = TrafficReportMessage.deserialize(
        b"\x7E\x14\x00\xAB\x45\x49\x1F\xEF\x15\xA8\x89\x78\x0F\x09\xA9\x07\xB0\x01\x20\x01\x4E\x38\x32\x35\x56\x20\x20\x20\x00\x57\xD6\x7e"
    )

    assert tr.traffic_alert is False
    assert tr.address_type == AddressType.ads_b_icao
    assert tr.address == int("52642511", 8)
    pytest.approx(tr.latitude, 44.90708)
    pytest.approx(tr.longitude, -122.99488)
    assert tr.track_type == TrackType.true_track_angle
    assert tr.report_extrapolated is False
    assert tr.airborne is True
    assert tr.integrity == Integrity.less_than_25_m_hpl_and_37_5_m_vpl
    assert tr.accuracy == Accuracy.less_than_30_m_hfom_and_45_m_vfom
    assert tr.horizontal_velocity == 123
    assert tr.vertical_velocity == 64
    assert tr.track == 45
    assert tr.emitter_category == EmitterCategory.light
    assert tr.callsign == "N825V"
    assert tr.emergency_priority_code == EmergencyPriorityCode.no_emergency
