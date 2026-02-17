from quantum.simulator import LocalQuantumSimulator, QuantumJob


def test_hadamard_distribution_is_deterministic_split():
    sim = LocalQuantumSimulator()
    result = sim.run(QuantumJob(qubits=1, gate="hadamard", shots=10))
    assert result == {"0": 5, "1": 5}
