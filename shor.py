from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import partial_trace

def shor_encode(n_qubits, state_vectors):
    """
    Initializes a quantum circuit with a given state vector and applies Shor encoding.

    Args:
        n_qubits (int): Number of logical qubits.
        state_vectors (list or numpy array): List of state vectors to initialize the circuit with.

    Returns:
        QuantumCircuit: The initialized and encoded quantum circuit.
    """
    qr = QuantumRegister(9 * n_qubits)
    cr = ClassicalRegister(3 * n_qubits)
    qc = QuantumCircuit(qr, cr)
    
    # Initialize the state vector on the primary wires
    for i in range(n_qubits):
        qc.initialize(state_vectors[i], [qr[9 * i]])

    qc.barrier()
    
    # Perform Shor encoding
    for qubit in range(n_qubits):
        start = qubit * 9
        # Encode the logical qubit
        qc.h(qr[start])
        qc.cx(qr[start], qr[start + 3])
        qc.cx(qr[start], qr[start + 6])
        
        for i in range(3):
            qc.cx(qr[start + i * 3], qr[start + i * 3 + 1])
            qc.cx(qr[start + i * 3], qr[start + i * 3 + 2])
        
        # Apply Hadamard gates to handle phase flip errors
        qc.h([qr[start], qr[start + 3], qr[start + 6]])

    qc.barrier()
    return qc


def shor_decode(n_qubits=1):
    """Creates a Shor decoding circuit for n qubits."""
    qr = QuantumRegister(9 * n_qubits)
    cr = ClassicalRegister(3 * n_qubits)
    qc = QuantumCircuit(qr, cr, name='Decoding')
    
    for qubit in range(n_qubits):
        start = qubit * 9
        # Apply Hadamard gates to handle phase flip errors
        qc.h([qr[start], qr[start + 3], qr[start + 6]])
        
        # Correct bit flip errors
        for i in range(3):
            qc.cx(qr[start + i * 3], qr[start + i * 3 + 1])
            qc.cx(qr[start + i * 3], qr[start + i * 3 + 2])
        
        qc.cx(qr[start], qr[start + 3])
        qc.cx(qr[start], qr[start + 6])
        qc.h(qr[start])
        
        # Measure the ancilla qubits
        # qc.measure([qr[start + 1], qr[start + 2], qr[start + 4], qr[start + 5], qr[start + 7], qr[start + 8]], 
                   # [cr[3 * qubit], cr[3 * qubit + 1], cr[3 * qubit + 2]])
    
    qc.barrier()
    return qc


def trace_over_ancilla_qubits(statevector, n_qubits=1):
    """Reduces the statevector from the 9*n_qubit system 
    to the n_qubit system by taking a partial trace over auxiliary qubits."""
    total_qubits = 9 * n_qubits
    keep_indices = [i * 9 for i in range(n_qubits)]
    trace_indices = [i for i in range(total_qubits) if i not in keep_indices]
    reduced_state = partial_trace(statevector, trace_indices)
    return reduced_state
    