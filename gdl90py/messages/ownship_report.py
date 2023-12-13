from __future__ import annotations

from dataclasses import dataclass

from gdl90py.messages._base_traffic_report import BaseTrafficReport


@dataclass(frozen=True)
class OwnshipReportMessage(BaseTrafficReport):
    MESSAGE_IDS = (10,)
