from __future__ import annotations

from dataclasses import dataclass

from gdl90py.messages._base_uat_report import BaseUATReportMessage


@dataclass(frozen=True)
class UplinkDataMessage(BaseUATReportMessage):
    MESSAGE_IDS = (7,)

    UPLINK_PAYLOAD_BITS = 432 * 8
