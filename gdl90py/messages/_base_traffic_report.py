from __future__ import annotations

from dataclasses import dataclass

from bitstring import BitArray

import gdl90py.gdl90_helpers
from gdl90py.bitarray_helpers import pop_bits
from gdl90py.enums import (
    Accuracy,
    AddressType,
    EmergencyPriorityCode,
    EmitterCategory,
    Integrity,
    TrackType,
)
from gdl90py.exceptions import DataTooLong, InvalidCallsign
from gdl90py.messages._base_message import BaseMessage


@dataclass(frozen=True)
class BaseTrafficReport(BaseMessage):
    traffic_alert: bool
    """
    Whether there is an active traffic alert for this target
    """
    address_type: AddressType
    """
    Target address type
    """
    address: int
    """
    24-bit target address
    """
    latitude: float
    """
    Target latitude in degrees
    """
    longitude: float
    """
    Target longitude in degrees
    """
    pressure_altitude: int | None
    """
    Target pressure altitude in feet
    """
    track_type: TrackType
    """
    Target track type
    """
    report_extrapolated: bool
    """
    True indicates the report is extrapolated.
    False indictaes the report is updated.
    """
    airborne: bool
    """
    Whether the target is airborne.
    """
    integrity: Integrity
    """
    Integrity of the data source
    """
    accuracy: Accuracy
    """
    Accuracy of the data source
    """
    horizontal_velocity: int | None
    """
    Target horizontal velocity in knots
    """
    vertical_velocity: int | None
    """
    Target horizontal velocity in feet per minute
    """
    track: int
    """
    Target track/heading in degrees
    """
    emitter_category: EmitterCategory
    """
    Target emitter type
    """
    callsign: str | None
    """
    8 character ASCII string callsign of the target
    """
    emergency_priority_code: EmergencyPriorityCode
    """
    Target emergency code
    """

    # constants
    TRAFFIC_ALERT_BITS = 4
    ADDRESS_TYPE_BITS = 4
    ADDRESS_BITS = 24
    LATITUDE_BITS = 24
    LATITUDE_MAX = 90
    LATITUDE_MIN = -90
    LONGITUDE_BITS = 24
    LONGITUDE_MAX = 180
    LONGITUDE_MIN = -180
    LATLON_RESOLUTION = 180 / (2**23)
    PRESSURE_ALTITUDE_BITS = 12
    PRESSURE_ALTITUDE_RESOLUTION = 25
    PRESSURE_ALTITUDE_OFFSET = 1000
    PRESSURE_ALTITUDE_MINIMUM = -1000
    PRESSURE_ALTITUDE_INVALID_VALUE = 0xFFF
    TRACK_TYPE_BITS = 2
    INTEGRITY_BITS = 4
    ACCURACY_BITS = 4
    HORIZONTAL_VELOCITY_BITS = 12
    HORIZONTAL_VELOCITY_MAX = 4094
    HORIZONTAL_VELOCITY_MAX_VALUE = 0xFFE
    HORIZONTAL_VELOCITY_INVALID = 0xFFF
    VERTICAL_VELOCITY_BITS = 12
    VERTICAL_VELOCITY_RESOLUTION = 64
    VERTICAL_VELOCITY_INVALID = 0x800
    VERTICAL_VELOCITY_MAX = 32576
    VERTICAL_VELOCITY_MIN = -32576
    VERTICAL_VELOCITY_MAX_VALUE = 32640
    VERTICAL_VELOCITY_MIN_VALUE = -32640
    TRACK_BITS = 8
    TRACK_RESOLUTION = 360 / 256
    EMITTER_CATEGORY_BITS = 8
    CALLSIGN_BITS = 64
    EMERGENCY_PRIORITY_CODE_BITS = 4
    RESERVED_BITS = 4

    @classmethod
    def _deserialize_traffic_alert(cls, traffic_alert_bitarray: BitArray) -> bool:
        # traffic_alert_bitarray is 4 bits long
        return traffic_alert_bitarray[0]

    def _serialize_traffic_alert(self) -> BitArray:
        return self._serialize_uint(int(self.traffic_alert), self.TRAFFIC_ALERT_BITS)

    @classmethod
    def _deserialize_address_type(cls, address_type_bitarray: BitArray) -> AddressType:
        return cls._deserialize_enum(address_type_bitarray, AddressType)

    def _serialize_address_type(self) -> BitArray:
        return self._serialize_enum(self.address_type, self.ADDRESS_TYPE_BITS)

    @classmethod
    def _deserialize_address(cls, address_bitarray: BitArray) -> int:
        return cls._deserialize_uint(address_bitarray)

    def _serialize_address(self) -> BitArray:
        return self._serialize_uint(self.address, self.ADDRESS_BITS, constrain=False)

    @classmethod
    def _deserialize_latitude(cls, latitude_bitarray: BitArray) -> float:
        return cls._deserialize_resolution_float(
            latitude_bitarray, cls.LATLON_RESOLUTION
        )

    def _serialize_latitude(self) -> BitArray:
        latitude = self.latitude
        if not (self.LATITUDE_MIN <= latitude <= self.LATITUDE_MAX):
            latitude = 0

        if self.integrity == Integrity.unknown:
            latitude = 0

        return self._serialize_resolution_float(
            latitude, self.LATLON_RESOLUTION, self.LATITUDE_BITS
        )

    @classmethod
    def _deserialize_longitude(cls, longitude_bitarray: BitArray) -> float:
        return cls._deserialize_resolution_float(
            longitude_bitarray, cls.LATLON_RESOLUTION
        )

    def _serialize_longitude(self) -> BitArray:
        longitude = self.longitude
        if not (self.LONGITUDE_MIN <= longitude <= self.LONGITUDE_MAX):
            longitude = 0

        if self.integrity == Integrity.unknown:
            longitude = 0

        return self._serialize_resolution_float(
            longitude, self.LATLON_RESOLUTION, self.LONGITUDE_BITS
        )

    @classmethod
    def _deserialize_pressure_altitude(
        cls, pressure_altitude_bitarray: BitArray
    ) -> int | None:
        if pressure_altitude_bitarray.uint == cls.PRESSURE_ALTITUDE_INVALID_VALUE:
            return None

        return cls._deserialize_resolution_offset_uint(
            pressure_altitude_bitarray,
            cls.PRESSURE_ALTITUDE_OFFSET,
            cls.PRESSURE_ALTITUDE_RESOLUTION,
        )

    def _serialize_pressure_altitude(self) -> BitArray:
        if self.pressure_altitude is None or not (
            self.PRESSURE_ALTITUDE_MINIMUM <= self.pressure_altitude
        ):
            return self._serialize_uint(
                self.PRESSURE_ALTITUDE_INVALID_VALUE, self.PRESSURE_ALTITUDE_BITS
            )

        return self._serialize_resolution_offset_uint(
            self.pressure_altitude,
            self.PRESSURE_ALTITUDE_OFFSET,
            self.PRESSURE_ALTITUDE_RESOLUTION,
            self.PRESSURE_ALTITUDE_BITS,
        )

    @classmethod
    def _deserialize_track_type(cls, track_type_bitarray: BitArray) -> TrackType:
        return cls._deserialize_enum(track_type_bitarray, TrackType)

    def _serialize_track_type(self) -> BitArray:
        return self._serialize_enum(self.track_type, self.TRACK_TYPE_BITS)

    @classmethod
    def _deserialize_report_extrapolated(
        cls, report_extrapolated_bitarray: BitArray
    ) -> bool:
        return cls._deserialize_bool(report_extrapolated_bitarray)

    def _serialize_report_extrapolated(self) -> BitArray:
        return self._serialize_bool(self.report_extrapolated)

    @classmethod
    def _deserialize_airborne(cls, airborne_bitarray: BitArray) -> bool:
        return cls._deserialize_bool(airborne_bitarray)

    def _serialize_airborne(self) -> BitArray:
        return self._serialize_bool(self.airborne)

    @classmethod
    def _deserialize_integrity(cls, integrity_bitarray: BitArray) -> Integrity:
        return cls._deserialize_enum(integrity_bitarray, Integrity)

    def _serialize_integrity(self) -> BitArray:
        return self._serialize_enum(self.integrity, self.INTEGRITY_BITS)

    @classmethod
    def _deserialize_accuracy(cls, accuracy_bitarray: BitArray) -> Accuracy:
        return cls._deserialize_enum(accuracy_bitarray, Accuracy)

    def _serialize_accuracy(self) -> BitArray:
        return self._serialize_enum(self.accuracy, self.ACCURACY_BITS)

    def _serialize_horizontal_velocity(self) -> BitArray:
        horizontal_velocity = self.horizontal_velocity
        if horizontal_velocity is None:
            return self._serialize_uint(
                self.HORIZONTAL_VELOCITY_INVALID, self.HORIZONTAL_VELOCITY_BITS
            )

        if horizontal_velocity > self.HORIZONTAL_VELOCITY_MAX:
            horizontal_velocity = self.HORIZONTAL_VELOCITY_MAX_VALUE

        return self._serialize_uint(horizontal_velocity, self.HORIZONTAL_VELOCITY_BITS)

    @classmethod
    def _deserialize_horizontal_velocity(
        cls, horizontal_velocity_bitarray: BitArray
    ) -> int | None:
        if horizontal_velocity_bitarray.uint == cls.HORIZONTAL_VELOCITY_INVALID:
            return None

        return cls._deserialize_uint(horizontal_velocity_bitarray)

    def _serialize_vertical_velocity(self) -> BitArray:
        vertical_velocity = self.vertical_velocity
        if vertical_velocity is None:
            return self._serialize_uint(
                self.VERTICAL_VELOCITY_INVALID, self.VERTICAL_VELOCITY_BITS
            )

        if vertical_velocity > self.VERTICAL_VELOCITY_MAX:
            vertical_velocity = self.VERTICAL_VELOCITY_MAX_VALUE

        if vertical_velocity < self.VERTICAL_VELOCITY_MIN:
            vertical_velocity = self.VERTICAL_VELOCITY_MIN_VALUE

        return self._serialize_resolution_int(
            vertical_velocity,
            self.VERTICAL_VELOCITY_RESOLUTION,
            self.VERTICAL_VELOCITY_BITS,
        )

    @classmethod
    def _deserialize_vertical_velocity(
        cls, vertical_velocity_bitarray: BitArray
    ) -> int | None:
        if vertical_velocity_bitarray.uint == cls.VERTICAL_VELOCITY_INVALID:
            return None

        return cls._deserialize_resolution_int(
            vertical_velocity_bitarray, cls.VERTICAL_VELOCITY_RESOLUTION
        )

    def _serialize_track(self) -> BitArray:
        return self._serialize_resolution_uint(
            self.track, self.TRACK_RESOLUTION, self.TRACK_BITS
        )

    @classmethod
    def _deserialize_track(cls, track_bitarray: BitArray) -> int:
        return cls._deserialize_resolution_uint(track_bitarray, cls.TRACK_RESOLUTION)

    @classmethod
    def _deserialize_emitter_category(
        cls, emitter_category_bitarray: BitArray
    ) -> EmitterCategory:
        return cls._deserialize_enum(emitter_category_bitarray, EmitterCategory)

    def _serialize_emitter_category(self) -> BitArray:
        return self._serialize_enum(self.emitter_category, self.EMITTER_CATEGORY_BITS)

    def _serialize_callsign(self) -> BitArray:
        callsign = self.callsign
        if callsign is None:
            callsign = " " * self.CALLSIGN_BITS

        # force upper case
        callsign = callsign.upper()[: self.CALLSIGN_BITS]

        # make sure characters are alphanumeric
        if not callsign.isalnum():
            raise InvalidCallsign("Invalid callsign. It contains illegal characters.")

        # this pads to the right as needed
        return self._serialize_str(callsign, self.CALLSIGN_BITS)

    @classmethod
    def _deserialize_callsign(cls, callsign_bitarray: BitArray) -> str:
        # remove trailing whitespace
        return cls._deserialize_str(callsign_bitarray).rstrip()

    @classmethod
    def _deserialize_emergency_priority_code(
        cls, emergency_priority_code_bitarray: BitArray
    ) -> EmergencyPriorityCode:
        return cls._deserialize_enum(
            emergency_priority_code_bitarray, EmergencyPriorityCode
        )

    def _serialize_emergency_priority_code(self) -> BitArray:
        return self._serialize_enum(
            self.emergency_priority_code, self.EMERGENCY_PRIORITY_CODE_BITS
        )

    def serialize(self, outgoing_lsb: bool = True) -> bytes:
        all_data = (
            self._serialize_traffic_alert()
            + self._serialize_address_type()
            + self._serialize_address()
            + self._serialize_latitude()
            + self._serialize_longitude()
            + self._serialize_pressure_altitude()
            + self._serialize_airborne()
            + self._serialize_report_extrapolated()
            + self._serialize_track_type()
            + self._serialize_integrity()
            + self._serialize_accuracy()
            + self._serialize_horizontal_velocity()
            + self._serialize_vertical_velocity()
            + self._serialize_track()
            + self._serialize_emitter_category()
            + self._serialize_callsign()
            + self._serialize_emergency_priority_code()
            + BitArray(uint=0, length=self.RESERVED_BITS)  # reserved
        )

        return gdl90py.gdl90_helpers.build(self.MESSAGE_IDS, all_data, outgoing_lsb)  # type: ignore

    @classmethod
    def deserialize(cls, data: BitArray) -> BaseTrafficReport:
        traffic_alert = cls._deserialize_traffic_alert(
            pop_bits(data, cls.TRAFFIC_ALERT_BITS)
        )
        address_type = cls._deserialize_address_type(
            pop_bits(data, cls.ADDRESS_TYPE_BITS)
        )
        address = cls._deserialize_address(pop_bits(data, cls.ADDRESS_BITS))
        latitude = cls._deserialize_latitude(pop_bits(data, cls.LATITUDE_BITS))
        longitude = cls._deserialize_longitude(pop_bits(data, cls.LONGITUDE_BITS))
        pressure_altitude = cls._deserialize_pressure_altitude(
            pop_bits(data, cls.PRESSURE_ALTITUDE_BITS)
        )
        airborne = cls._deserialize_airborne(pop_bits(data, 1))
        report_extrapolated = cls._deserialize_report_extrapolated(pop_bits(data, 1))
        track_type = cls._deserialize_track_type(pop_bits(data, cls.TRACK_TYPE_BITS))
        integrity = cls._deserialize_integrity(pop_bits(data, cls.INTEGRITY_BITS))
        accuracy = cls._deserialize_accuracy(pop_bits(data, cls.ACCURACY_BITS))
        horizontal_velocity = cls._deserialize_horizontal_velocity(
            pop_bits(data, cls.HORIZONTAL_VELOCITY_BITS)
        )
        vertical_velocity = cls._deserialize_vertical_velocity(
            pop_bits(data, cls.VERTICAL_VELOCITY_BITS)
        )
        track = cls._deserialize_track(pop_bits(data, cls.TRACK_BITS))
        emitter_category = cls._deserialize_emitter_category(
            pop_bits(data, cls.EMITTER_CATEGORY_BITS)
        )
        callsign = cls._deserialize_callsign(pop_bits(data, cls.CALLSIGN_BITS))
        emergency_priority_code = cls._deserialize_emergency_priority_code(
            pop_bits(data, cls.EMERGENCY_PRIORITY_CODE_BITS)
        )

        pop_bits(data, cls.RESERVED_BITS)

        if len(data) != 0:
            raise DataTooLong(f"Data is {len(data)} bits long")

        return cls(
            traffic_alert=traffic_alert,
            address_type=address_type,
            address=address,
            latitude=latitude,
            longitude=longitude,
            pressure_altitude=pressure_altitude,
            airborne=airborne,
            report_extrapolated=report_extrapolated,
            track_type=track_type,
            integrity=integrity,
            accuracy=accuracy,
            horizontal_velocity=horizontal_velocity,
            vertical_velocity=vertical_velocity,
            track=track,
            emitter_category=emitter_category,
            callsign=callsign,
            emergency_priority_code=emergency_priority_code,
        )
