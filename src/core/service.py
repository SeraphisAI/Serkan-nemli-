from __future__ import annotations
from dataclasses import dataclass, field
from statistics import mean
from typing import List

from core.models import SensorReading


@dataclass
class SensorService:
    readings: List[SensorReading] = field(default_factory=list)

    def ingest(self, reading: SensorReading) -> dict:
        self.readings.append(reading)
        return {"accepted": True, "count": len(self.readings)}

    def summary(self) -> dict:
        if not self.readings:
            return {"count": 0, "avg_temp": None, "avg_humidity": None}
        return {
            "count": len(self.readings),
            "avg_temp": round(mean(r.temperature_c for r in self.readings), 3),
            "avg_humidity": round(mean(r.humidity_pct for r in self.readings), 3),
        }
