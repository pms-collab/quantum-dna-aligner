# quantum/oracle.py
from qiskit import QuantumCircuit

def equality_oracle(target_bits: str):
    """
    target_bits: e.g. '0101' (len = n)
    Returns a QuantumCircuit implementing a phase-flip oracle
    that marks |x> with phase -1 iff x == target.
    Uses X gates to map target to |11..1| then multi-controlled Z trick.
    """
    n = len(target_bits)
    qc = QuantumCircuit(n+1, name="EqOracle")  # ancilla as phase flag (last qubit |->)
    # Prepare controls by flipping where target bit is '0'
    for i, b in enumerate(reversed(target_bits)):
        if b == '0':
            qc.x(i)
    # multi-controlled Z using ancilla as target
    qc.h(n)              # turn ancilla into |+>
    qc.mcx(list(range(n)), n)  # controlled X on ancilla
    qc.h(n)
    # uncompute flips
    for i, b in enumerate(reversed(target_bits)):
        if b == '0':
            qc.x(i)
    return qc

