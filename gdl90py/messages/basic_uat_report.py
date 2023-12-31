from __future__ import annotations

from dataclasses import dataclass

from gdl90py.messages._base_uat_report import BaseUATReportMessage


@dataclass(frozen=True)
class BasicUATReportMessage(BaseUATReportMessage):
    MESSAGE_IDS = (30,)

    UPLINK_PAYLOAD_BITS = 18 * 8
