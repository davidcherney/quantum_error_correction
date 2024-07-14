from qiskit.quantum_info import random_statevector
from qiskit.quantum_info import partial_trace

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

def trace_over_ancilla_qubits(statevector, n_qubits=1):
    """Reduces the statevector from the 9*n_qubit system 
    to the n_qubit system by taking a partial trace over auxiliary qubits.

    Args: 
        statevector (array): State vector with 2^{9*n_qubits}

    Returns:
        reduced_state (array)
    """
    total_qubits = 9 * n_qubits
    keep_indices = [i * 9 for i in range(n_qubits)]
    trace_indices = [i for i in range(total_qubits) if i not in keep_indices]
    reduced_state = partial_trace(statevector, trace_indices)
    return reduced_state