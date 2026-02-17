from dataclasses import dataclass


@dataclass
class SensorReading:
    sensor_id: str
    ts: int
    temperature_c: float
    humidity_pct: float
    location: str = "unknown"

    def __post_init__(self) -> None:
        if len(self.sensor_id) < 2:
            raise ValueError("sensor_id too short")

    def model_dump(self) -> dict:
        return self.__dict__.copy()


@dataclass
class UpdatePackage:
    version: str
    notes: str
    payload_sha256: str
    signature: str


@dataclass
class UpdateApplyRequest:
    package: UpdatePackage
    approver: str

    def __init__(self, package: dict | UpdatePackage, approver: str):
        self.package = package if isinstance(package, UpdatePackage) else UpdatePackage(**package)
        self.approver = approver
