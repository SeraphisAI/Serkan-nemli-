from __future__ import annotations
from dataclasses import dataclass


@dataclass
class QuantumJob:
    qubits: int
    gate: str
    shots: int = 128


class LocalQuantumSimulator:
    def run(self, job: QuantumJob) -> dict:
        if job.gate == "hadamard":
            zeros = job.shots // 2
            ones = job.shots - zeros
            return {"0": zeros, "1": ones}
        if job.gate == "x":
            return {"1": job.shots}
        return {"0": job.shots}


class QPUProviderAdapter:
    def submit(self, job: QuantumJob) -> str:
        return f"stub-job-{job.qubits}-{job.gate}"
