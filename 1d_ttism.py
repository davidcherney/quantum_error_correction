from qiskit import QuantumCircuit
from qiskit.circuit.library import YGate, UnitaryGate # latter allows creation of new unitary gates
import numpy as np

# Defne the square root of Y gate and square root of Y dagger gate in terms of YGate.
SYGate = UnitaryGate(YGate().power(1/2), label=r"$\sqrt{Y}$")
SYdgGate = UnitaryGate(SYGate.inverse(), label=r"$\sqrt{Y}^\dag$")

def generate_1d_tfim_circuit(num_qubits, num_trotter_steps, rx_angle, 
                             num_cl_bits=0, # Classical bits are used to report measurements
                             trotter_barriers = False, # Draw a vertical line between trotter steps.
                             layer_barriers = False # Draw a vertical line between Layers in the 2-qubit layering of 2-qubit depth
                            ):
    '''tfim means Transverse field ising model'''
    if num_cl_bits == 0:
        qc = QuantumCircuit(num_qubits)
    else:
        qc = QuantumCircuit(num_qubits, 
                            num_cl_bits # These are where measurements will go.
                           )

    for trotter_step in range(num_trotter_steps):
        add_1d_tfim_trotter_layer(qc, rx_angle, layer_barriers)
        if trotter_barriers:
            # 
            qc.barrier()
    
    return qc

def add_1d_tfim_trotter_layer(qc, rx_angle, layer_barriers = False):
    # Apply Rzz in the red/even layer
    for i in range(0, qc.num_qubits-1, 2): # note that is every other index
        # Apply gates as in the diagram:
        qc.sdg([i, i+1]) # sdg is s dagger 
        qc.append(SYGate, [i+1]) # SYGate appears to be a name for square root of Y
        qc.cx(i, i+1) # controlled swap
        qc.append(SYdgGate, [i+1]) # square root of Y dagger
    if layer_barriers:
        # In the diagram we will draw, put all gates applied so far to the left of a barrier
        # and everything that follows to the right of the barrier. 
        qc.barrier() 
    # Apply Rzz in the green/odd layers
    for i in range(1, qc.num_qubits-1, 2): #start at 1 not at 0
        qc.sdg([i, i+1])
        qc.append(SYGate, [i+1])
        qc.cx(i, i+1)
        qc.append(SYdgGate, [i+1])
    if layer_barriers:
        qc.barrier()
    # Apply Rx in all vertices
    qc.rx(rx_angle, list(range(qc.num_qubits)))
    if layer_barriers:
        qc.barrier()


# Code up the circuit going backward.

def append_mirrored_1d_tfim_circuit(
    qc, num_qubits, num_trotter_steps, rx_angle, 
    trotter_barriers = False, layer_barriers = False
    ):
    for trotter_step in range(num_trotter_steps):
        add_mirrored_1d_tfim_trotter_layer(qc, rx_angle, layer_barriers)
        if trotter_barriers:
            qc.barrier()

def add_mirrored_1d_tfim_trotter_layer(qc, rx_angle, layer_barriers = False):
    # Note after filming:
    # I constructed the inverse by hand here
    # But you could also use QuantumCircuit.inverse() to do this more efficiently
    # R_x first
    qc.rx(-rx_angle, list(range(qc.num_qubits)))
    if layer_barriers:
        qc.barrier()
    # Adding Rzz in the odd/green layers second
    for i in range(1, qc.num_qubits-1, 2):
        qc.append(SYGate, [i+1])
        qc.cx(i, i+1)
        qc.append(SYdgGate, [i+1])
        qc.s([i, i+1])
    if layer_barriers:
        qc.barrier()
    # Adding Rzz in the even/red layers last
    for i in range(0, qc.num_qubits-1, 2):
        qc.append(SYGate, [i+1])
        qc.cx(i, i+1)
        qc.append(SYdgGate, [i+1])
        qc.s([i, i+1])
    if layer_barriers:
        qc.barrier()