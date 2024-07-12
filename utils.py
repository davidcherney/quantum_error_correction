from qiskit.quantum_info import random_statevector

def generate_random_states(n_qubits):
    """
    Generates random state vectors for the given number of qubits.

    Args:
        n_qubits (int): Number of qubits.

    Returns:
        list: List of random state vectors.
    """
    state_vectors = [random_statevector(2) for _ in range(n_qubits)]
    return state_vectors