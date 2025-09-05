#!/usr/bin/env python3
import argparse, math, random
from qiskit import QuantumCircuit, Aer, execute
from oracle import equality_oracle

ENC = {'A':'00','C':'01','G':'10','T':'11'}

def dna_to_bits(s: str) -> str:
    return "".join(ENC[c] for c in s)

def load_query(path):
    with open(path) as f:
        for line in f:
            if line.startswith(">"): continue
            l=line.strip()
            if l: return l

def pick_target_from_db(db_path, q):
    # q와 같은 k-mer가 존재한다고 가정하고 하나 고름
    with open(db_path) as f:
        candidates=[line.strip().split("\t")[0] for line in f]
    if q in candidates:
        return q
    # 없으면 데모를 위해 q를 그냥 타깃으로 씀
    return q

def grover_once(target_bits, shots=2048):
    n = len(target_bits)
    anc = 1
    qc = QuantumCircuit(n+anc, n)

    # init superposition for search register
    for i in range(n):
        qc.h(i)
    # ancilla to |->
    # (여기선 ancilla를 Z phase flip 용도로 쓰지 않고, oracle 내부에서 phase 처리)
    qc.x(n); qc.h(n)

    # oracle
    oracle = equality_oracle(target_bits)
    qc.compose(oracle, qubits=list(range(n+1)), inplace=True)

    # diffusion
    for i in range(n):
        qc.h(i); qc.x(i)
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    for i in range(n):
        qc.x(i); qc.h(i)

    # unprepare ancilla
    qc.h(n); qc.x(n)

    # measure search register only
    qc.measure(range(n), range(n))

    backend = Aer.get_backend("qasm_simulator")
    job = execute(qc, backend=backend, shots=shots)
    return job.result().get_counts()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--db", required=True)
    ap.add_argument("--shots", type=int, default=2048)
    args = ap.parse_args()

    q = load_query(args.query)
    target = pick_target_from_db(args.db, q)
    bits = dna_to_bits(target)

    # n qubits = 2 * k
    counts = grover_once(bits, shots=args.shots)
    # 최빈값 확인
    top = max(counts.items(), key=lambda x: x[1])
    print(f"[grover] target_kmer={target} target_bits={bits} top_state={top[0]} hits={top[1]}/{sum(counts.values())}")

if __name__ == "__main__":
    main()

