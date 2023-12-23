from __future__ import annotations

from dataclasses import dataclass

from gdl90py.messages._base_uat_report import BaseUATReportMessage


@dataclass(frozen=True)
class LongUATReportMessage(BaseUATReportMessage):
    MESSAGE_IDS = (31,)

    UPLINK_PAYLOAD_BITS = 34 * 8
