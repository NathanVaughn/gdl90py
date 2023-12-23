import pytest
from bitstring import BitArray

from gdl90py.enums import (
    Accuracy,
    AddressType,
    EmergencyPriorityCode,
    EmitterCategory,
    Integrity,
    TrackType,
)
from gdl90py.exceptions import DataTooLong, InvalidCallsign
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


@pytest.mark.parametrize("latitude", (-91, 91, -90.0000001, 90.0000001))
def test_traffic_report_serialize_invalid_latitude(latitude: float):
    tr = TrafficReportMessage(
        traffic_alert=False,
        address_type=AddressType.ads_b_icao,
        address=int("52642511", 8),
        latitude=latitude,
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
    assert tr.serialize(outgoing_lsb=False)[6:9] == b"\x00\x00\x00"


@pytest.mark.parametrize("longitude", (-181, 181, -180.0000001, 180.0000001))
def test_traffic_report_serialize_invalid_longitude(longitude: float):
    tr = TrafficReportMessage(
        traffic_alert=False,
        address_type=AddressType.ads_b_icao,
        address=int("52642511", 8),
        latitude=44.90708,
        longitude=longitude,
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
    assert tr.serialize(outgoing_lsb=False)[9:12] == b"\x00\x00\x00"


@pytest.mark.parametrize(
    "pressure_altitude, expected",
    (
        (-5000, b"\x00\x00"),
        (-1000, b"\x00\x00"),
        (0, b"\x02\x80"),
        (1000, b"\x05\x00"),
        (101350, b"\xFF\xE0"),
        (200000, b"\xFF\xE0"),
        (None, b"\xFF\xF0"),
    ),
)
def test_traffic_report_serialize_pressure_altitude(
    pressure_altitude: int, expected: bytes
):
    tr = TrafficReportMessage(
        traffic_alert=False,
        address_type=AddressType.ads_b_icao,
        address=int("52642511", 8),
        latitude=44.90708,
        longitude=-122.99488,
        pressure_altitude=pressure_altitude,
        track_type=TrackType.invalid,
        report_extrapolated=False,
        airborne=False,
        integrity=Integrity.less_than_25_m_hpl_and_37_5_m_vpl,
        accuracy=Accuracy.less_than_30_m_hfom_and_45_m_vfom,
        horizontal_velocity=123,
        vertical_velocity=64,
        track=45,
        emitter_category=EmitterCategory.light,
        callsign="N825V",
        emergency_priority_code=EmergencyPriorityCode.no_emergency,
    )
    assert tr.serialize(outgoing_lsb=False)[12:14] == expected


@pytest.mark.parametrize(
    "pressure_altitude_bytes, expected",
    (
        (b"\x00\x00", -1000),
        (b"\x02\x80", 0),
        (b"\x05\x00", 1000),
        (b"\xFF\xE0", 101350),
        (b"\xFF\xF0", None),
    ),
)
def test_traffic_report_deserialize_pressure_altitude(
    pressure_altitude_bytes: bytes, expected: int
):
    assert (
        TrafficReportMessage.deserialize(
            BitArray(
                bytes=b"\x00\xAB\x45\x49\x1F\xEF\x15\xA8\x89\x78"
                + pressure_altitude_bytes
                + b"\xA9\x07\xB0\x01\x20\x01\x4E\x38\x32\x35\x56\x20\x20\x20\x00"
            )
        ).pressure_altitude
        == expected
    )


def test_traffic_report_serialize_integrity_unknown():
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
        integrity=Integrity.unknown,
        accuracy=Accuracy.less_than_30_m_hfom_and_45_m_vfom,
        horizontal_velocity=123,
        vertical_velocity=64,
        track=45,
        emitter_category=EmitterCategory.light,
        callsign="N825V",
        emergency_priority_code=EmergencyPriorityCode.no_emergency,
    )
    # check that latitude and longitude are 0
    assert tr.serialize(outgoing_lsb=False)[6:12] == b"\x00\x00\x00\x00\x00\x00"


@pytest.mark.parametrize(
    "horizontal_velocity, expected",
    (
        (0, b"\x00\x00"),
        (500, b"\x1F\x40"),
        (4094, b"\xFF\xE0"),
        (5000, b"\xFF\xE0"),
        (None, b"\xFF\xF0"),
    ),
)
def test_traffic_report_serialize_horizontal_velocity(
    horizontal_velocity: int, expected: bytes
):
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
        horizontal_velocity=horizontal_velocity,
        vertical_velocity=0,
        track=45,
        emitter_category=EmitterCategory.light,
        callsign="N825V",
        emergency_priority_code=EmergencyPriorityCode.no_emergency,
    )
    assert tr.serialize(outgoing_lsb=False)[15:17] == expected


@pytest.mark.parametrize(
    "horizontal_velocity_bytes, expected",
    (
        (b"\x00\x00", 0),
        (b"\x1F\x40", 500),
        (b"\xFF\xE0", 4094),
        (b"\xFF\xF0", None),
    ),
)
def test_traffic_report_deserialize_horizontal_velocity(
    horizontal_velocity_bytes: bytes, expected: int
):
    assert (
        TrafficReportMessage.deserialize(
            BitArray(
                bytes=b"\x00\xAB\x45\x49\x1F\xEF\x15\xA8\x89\x78\x0F\x09\xA9"
                + horizontal_velocity_bytes
                + b"\x01\x20\x01\x4E\x38\x32\x35\x56\x20\x20\x20\x00"
            )
        ).horizontal_velocity
        == expected
    )


@pytest.mark.parametrize(
    "vertical_velocity, expected",
    (
        (0, b"\x00\x00"),
        (64, b"\x00\x01"),
        (-64, b"\x0F\xFF"),
        (32576, b"\x01\xFD"),
        (40000, b"\x01\xFE"),
        (-32576, b"\x0E\x03"),
        (-40000, b"\x0E\x02"),
        (None, b"\x08\x00"),
    ),
)
def test_traffic_report_serialize_vertical_velocity(
    vertical_velocity: int, expected: bytes
):
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
        horizontal_velocity=0,
        vertical_velocity=vertical_velocity,
        track=45,
        emitter_category=EmitterCategory.light,
        callsign="N825V",
        emergency_priority_code=EmergencyPriorityCode.no_emergency,
    )
    assert tr.serialize(outgoing_lsb=False)[16:18] == expected


@pytest.mark.parametrize(
    "vertical_velocity_bytes, expected",
    (
        (b"\x00\x00", 0),
        (b"\x00\x01", 64),
        (b"\x0F\xFF", -64),
        (b"\x01\xFD", 32576),
        (b"\x0E\x03", -32576),
        (b"\x08\x00", None),
    ),
)
def test_traffic_report_deserialize_vertical_velocity(
    vertical_velocity_bytes: bytes, expected: int
):
    assert (
        TrafficReportMessage.deserialize(
            BitArray(
                bytes=b"\x00\xAB\x45\x49\x1F\xEF\x15\xA8\x89\x78\x0F\x09\xA9\x07"
                + vertical_velocity_bytes
                + b"\x20\x01\x4E\x38\x32\x35\x56\x20\x20\x20\x00"
            )
        ).vertical_velocity
        == expected
    )


@pytest.mark.parametrize(
    "callsign, expected",
    (
        ("N12345", b"N12345\x20\x20"),
        ("N1234567", b"N1234567"),
        ("abcdefgh", b"ABCDEFGH"),
        ("N12345678910", b"N1234567"),
        ("", b"\x20\x20\x20\x20\x20\x20\x20\x20"),
        (None, b"\x20\x20\x20\x20\x20\x20\x20\x20"),
    ),
)
def test_traffic_report_serialize_callsign(callsign: str, expected: bytes):
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
        callsign=callsign,
        emergency_priority_code=EmergencyPriorityCode.no_emergency,
    )
    assert tr.serialize(outgoing_lsb=False)[20:28] == expected


@pytest.mark.parametrize(
    "callsign_bytes, expected",
    (
        (b"\x20\x20\x20\x20\x20\x20\x20\x20", ""),
        (b"N12345\x20\x20", "N12345"),
        (b"ABCDEFGH", "ABCDEFGH"),
    ),
)
def test_traffic_report_deserialize_callsign(callsign_bytes: bytes, expected: int):
    assert (
        TrafficReportMessage.deserialize(
            BitArray(
                bytes=b"\x00\xAB\x45\x49\x1F\xEF\x15\xA8\x89\x78\x0F\x09\xA9\x07\xB0\x01\x20\x01"
                + callsign_bytes
                + b"\x00"
            )
        ).callsign
        == expected
    )


@pytest.mark.parametrize(
    "callsign",
    (("!", "~", ",", "()", "adsas_56", "ab cd")),
)
def test_traffic_report_serialize_invalid_callsign(callsign: str):
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
        callsign=callsign,
        emergency_priority_code=EmergencyPriorityCode.no_emergency,
    )
    with pytest.raises(InvalidCallsign):
        tr.serialize(outgoing_lsb=False)


def test_traffic_report_deserialize_too_long():
    with pytest.raises(DataTooLong):
        TrafficReportMessage.deserialize(
            b"\x7E\x14\x00\xAB\x45\x49\x1F\xEF\x15\xA8\x89\x78\x0F\x09\xA9\x07\xB0\x01\x20\x01\x4E\x38\x32\x35\x56\x20\x20\x20\x00\x00\xbb\xfc\x7e"
        )
