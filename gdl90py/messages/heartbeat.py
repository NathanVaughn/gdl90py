from __future__ import annotations

import datetime
from dataclasses import dataclass

from bitstring import BitArray

import gdl90py.gdl90_helpers
from gdl90py.bitarray_helpers import pop_bits
from gdl90py.exceptions import DataTooLong
from gdl90py.messages._base_message import BaseMessage

SECONDS_PER_MINUTE = 60
MINUTES_PER_HOUR = 60
SECONDS_PER_HOUR = SECONDS_PER_MINUTE * MINUTES_PER_HOUR


@dataclass(frozen=True)
class HeartbeatMessage(BaseMessage):
    MESSAGE_IDS = (0,)

    gps_position_valid: bool
    """
    Whether the GPS position is valid.
    """
    maintenance_required: bool
    """
    Whether a problem that requires maintenance has been detected.
    ForeFlight ignores this.
    """
    ident_talkback: bool
    """
    Whether the IDENT indification has been set in transmitted ADS-B messages.
    ForeFlight ignores this.
    """
    self_assigned_address_talkback: bool
    """
    Whether a self-assigned ADS-B address is being used.
    ForeFlight ignores this.
    """
    gps_battery_low: bool
    """
    Indicates if the internal GPS battery is low.
    ForeFlight ignores this.
    """
    RATCS_talkback: bool
    """
    Whether Receiving ATC Services has been set in transmitted ADS-B messages.
    ForeFlight ignores this.
    """
    UAT_initialized: bool
    """
    Whether the Universal Access Transceiver has been initialized. Should be True.
    ForeFlight ignores this.
    """
    CSA_requested: bool
    """
    Whether Conflict Situational Awareness has been requested.
    ForeFlight ignores this.
    """
    CSA_unavailable: bool
    """
    Whether Conflict Situational Awareness has been requested and is not available.
    ForeFlight ignores this.
    """
    UTC_timing_valid: bool
    """
    Whether a valid UTC timing refernce is being used.
    ForeFlight ignores this.
    """
    timestamp: datetime.time
    """
    UTC timestamp of the message. Can be generated with datetime.datetime.now(datetime.UTC)
    ForeFlight ignores this.
    """
    uplink_messages_count: int
    """
    Number of uplink messages recieved in the previous second.
    ForeFlight ignores this.
    """
    basic_long_messages_count: int
    """
    Number of Basic and Long messages recieved in the previous second.
    ForeFlight ignores this.
    """

    TIMESTAMP_BITS_1 = 1
    TIMESTAMP_BITS_2 = 8
    TIMESTAMP_BITS_3 = 8
    TIMESTAMP_BITS = TIMESTAMP_BITS_1 + TIMESTAMP_BITS_2 + TIMESTAMP_BITS_3
    UPLINK_MESSAGES_COUNT_BITS = 5
    BASIC_LONG_MESSAGES_COUNT_BITS = 10

    RESERVED_1_BITS = 1
    RESERVED_2_BITS = 4
    RESERVED_3_BITS = 1

    def _serialize_gps_position_valid(self) -> BitArray:
        return self._serialize_bool(self.gps_position_valid)

    @classmethod
    def _deserialize_gps_position_valid(
        cls, gps_position_valid_bitarray: BitArray
    ) -> bool:
        return cls._deserialize_bool(gps_position_valid_bitarray)

    def _serialize_maintenance_required(self) -> BitArray:
        return self._serialize_bool(self.maintenance_required)

    @classmethod
    def _deserialize_maintenance_required(
        cls, maintenance_required_bitarray: BitArray
    ) -> bool:
        return cls._deserialize_bool(maintenance_required_bitarray)

    def _serialize_ident_talkback(self) -> BitArray:
        return self._serialize_bool(self.ident_talkback)

    @classmethod
    def _deserialize_ident_talkback(cls, ident_talkback_bitarray: BitArray) -> bool:
        return cls._deserialize_bool(ident_talkback_bitarray)

    def _serialize_self_assigned_address_talkback(self) -> BitArray:
        return self._serialize_bool(self.self_assigned_address_talkback)

    @classmethod
    def _deserialize_self_assigned_address_talkback(
        cls, self_assigned_address_talkback_bitarray: BitArray
    ) -> bool:
        return cls._deserialize_bool(self_assigned_address_talkback_bitarray)

    def _serialize_gps_battery_low(self) -> BitArray:
        return self._serialize_bool(self.gps_battery_low)

    @classmethod
    def _deserialize_gps_battery_low(cls, gps_battery_low_bitarray: BitArray) -> bool:
        return cls._deserialize_bool(gps_battery_low_bitarray)

    def _serialize_RATCS_talkback(self) -> BitArray:
        return self._serialize_bool(self.RATCS_talkback)

    @classmethod
    def _deserialize_RATCS_talkback(cls, RATCS_talkback_bitarray: BitArray) -> bool:
        return cls._deserialize_bool(RATCS_talkback_bitarray)

    def _serialize_UAT_initialized(self) -> BitArray:
        return self._serialize_bool(self.UAT_initialized)

    @classmethod
    def _deserialize_UAT_initialized(cls, UAT_initialized_bitarray: BitArray) -> bool:
        return cls._deserialize_bool(UAT_initialized_bitarray)

    def _serialize_CSA_requested(self) -> BitArray:
        return self._serialize_bool(self.CSA_requested)

    @classmethod
    def _deserialize_CSA_requested(cls, CSA_requested_bitarray: BitArray) -> bool:
        return cls._deserialize_bool(CSA_requested_bitarray)

    def _serialize_CSA_unavailable(self) -> BitArray:
        return self._serialize_bool(self.CSA_unavailable)

    @classmethod
    def _deserialize_CSA_unavailable(cls, CSA_unavailable_bitarray: BitArray) -> bool:
        return cls._deserialize_bool(CSA_unavailable_bitarray)

    def _serialize_UTC_timing_valid(self) -> BitArray:
        return self._serialize_bool(self.UTC_timing_valid)

    @classmethod
    def _deserialize_UTC_timing_valid(cls, UTC_timing_valid_bitarray: BitArray) -> bool:
        return cls._deserialize_bool(UTC_timing_valid_bitarray)

    def _serialize_timestamp(self) -> BitArray:
        total_seconds = (
            (self.timestamp.hour * SECONDS_PER_HOUR)
            + (self.timestamp.minute * SECONDS_PER_MINUTE)
            + self.timestamp.second
        )
        return self._serialize_uint(total_seconds, self.TIMESTAMP_BITS)

    @classmethod
    def _deserialize_timestamp(cls, timestamp_bitarray: BitArray) -> datetime.time:
        total_seconds = cls._deserialize_uint(timestamp_bitarray)
        hours, remainder_seconds = divmod(total_seconds, SECONDS_PER_HOUR)
        minutes, seconds = divmod(remainder_seconds, SECONDS_PER_MINUTE)
        return datetime.time(
            hour=hours, minute=minutes, second=seconds, tzinfo=datetime.UTC
        )

    def _serialize_uplink_messages_count(self) -> BitArray:
        return self._serialize_uint(
            self.uplink_messages_count, self.UPLINK_MESSAGES_COUNT_BITS
        )

    @classmethod
    def _deserialize_uplink_messages_count(
        cls, uplink_messages_count_bitarray: BitArray
    ) -> int:
        return cls._deserialize_uint(uplink_messages_count_bitarray)

    def _serialize_basic_long_messages_count(self) -> BitArray:
        return self._serialize_uint(
            self.basic_long_messages_count, self.BASIC_LONG_MESSAGES_COUNT_BITS
        )

    @classmethod
    def _deserialize_basic_long_messages_count(
        cls, basic_long_messages_count_bitarray: BitArray
    ) -> int:
        return cls._deserialize_uint(basic_long_messages_count_bitarray)

    def serialize(self, outgoing_lsb: bool = True) -> bytes:
        timestamp_bitarray = self._serialize_timestamp()
        all_data = (
            self._serialize_gps_position_valid()
            + self._serialize_maintenance_required()
            + self._serialize_ident_talkback()
            + self._serialize_self_assigned_address_talkback()
            + self._serialize_gps_battery_low()
            + self._serialize_RATCS_talkback()
            + BitArray(uint=0, length=self.RESERVED_1_BITS)  # reserved
            + self._serialize_UAT_initialized()
            + timestamp_bitarray[: self.TIMESTAMP_BITS_1]
            + self._serialize_CSA_requested()
            + self._serialize_CSA_unavailable()
            + BitArray(uint=0, length=self.RESERVED_2_BITS)  # reserved
            + self._serialize_UTC_timing_valid()
            + timestamp_bitarray[self.TIMESTAMP_BITS_1 + self.TIMESTAMP_BITS_2 :]
            + timestamp_bitarray[
                self.TIMESTAMP_BITS_1 : self.TIMESTAMP_BITS_1 + self.TIMESTAMP_BITS_2
            ]
            + self._serialize_uplink_messages_count()
            + BitArray(uint=0, length=self.RESERVED_3_BITS)  # reserved
            + self._serialize_basic_long_messages_count()
        )
        return gdl90py.gdl90_helpers.build(self.MESSAGE_IDS, all_data, outgoing_lsb)

    @classmethod
    def deserialize(cls, data: BitArray) -> HeartbeatMessage:
        gps_position_valid = cls._deserialize_gps_position_valid(pop_bits(data, 1))
        maintenance_required = cls._deserialize_maintenance_required(pop_bits(data, 1))
        ident_talkback = cls._deserialize_ident_talkback(pop_bits(data, 1))
        self_assigned_address_talkback = (
            cls._deserialize_self_assigned_address_talkback(pop_bits(data, 1))
        )
        gps_battery_low = cls._deserialize_gps_battery_low(pop_bits(data, 1))
        RATCS_talkback = cls._deserialize_RATCS_talkback(pop_bits(data, 1))
        pop_bits(data, cls.RESERVED_1_BITS)  # reserved
        UAT_initialized = cls._deserialize_UAT_initialized(pop_bits(data, 1))

        timestamp_bits_1 = pop_bits(data, cls.TIMESTAMP_BITS_1)

        CSA_requested = cls._deserialize_CSA_requested(pop_bits(data, 1))
        CSA_unavailable = cls._deserialize_CSA_unavailable(pop_bits(data, 1))
        pop_bits(data, cls.RESERVED_2_BITS)  # reserved
        UTC_timing_valid = cls._deserialize_UTC_timing_valid(pop_bits(data, 1))

        timestamp_bits_2 = pop_bits(data, cls.TIMESTAMP_BITS_2)
        timestamp_bits_3 = pop_bits(data, cls.TIMESTAMP_BITS_3)
        timestamp = cls._deserialize_timestamp(
            timestamp_bits_1 + timestamp_bits_3 + timestamp_bits_2
        )
        uplink_messages_count = cls._deserialize_uplink_messages_count(
            pop_bits(data, cls.UPLINK_MESSAGES_COUNT_BITS)
        )
        pop_bits(data, cls.RESERVED_3_BITS)  # reserved
        basic_long_messages_count = cls._deserialize_basic_long_messages_count(
            pop_bits(data, cls.BASIC_LONG_MESSAGES_COUNT_BITS)
        )

        if len(data) != 0:
            raise DataTooLong(f"Data is {len(data)} bits long")

        return HeartbeatMessage(
            gps_position_valid=gps_position_valid,
            maintenance_required=maintenance_required,
            ident_talkback=ident_talkback,
            self_assigned_address_talkback=self_assigned_address_talkback,
            gps_battery_low=gps_battery_low,
            RATCS_talkback=RATCS_talkback,
            UAT_initialized=UAT_initialized,
            CSA_requested=CSA_requested,
            CSA_unavailable=CSA_unavailable,
            UTC_timing_valid=UTC_timing_valid,
            timestamp=timestamp,
            uplink_messages_count=uplink_messages_count,
            basic_long_messages_count=basic_long_messages_count,
        )
