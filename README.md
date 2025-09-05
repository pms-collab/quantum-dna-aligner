# quantum-dna-aligner
Proof-of-concept quantum-inspired seeding algorithm for DNA alignment.

**Goal.** Demonstrate a *query-complexity* advantage for k-mer seeding in DNA alignment using a Grover-style search subroutine, with clear classical baselines.

## Scope
We target the **seeding** stage of seed-and-extend alignment. Extension (Smith-Waterman / Needleman-Wunsch) is out of scope for quantum speedups in this POC.

## Claims & Non-Claims
- **Claim:** For a database of N k-mers with M true matches, our quantum subroutine achieves O(sqrt(N/M)) oracle queries(query-complexity) vs. O(N/M) for naive classical search, demonstrated on small synthetic datasets.
- **Non-Claims:** End-to-end wall-clock advantage on practical hardware; cost of oracle construction; superiority over optimized FM-index/hashtable pipelines. This POC does not compare against FM-index/FM-search or minimap2-class pipelines; only naive/hash baselines are reported.

## Methods
- **Baselines:** BL0 linear scan; BL1 simple hash lookup.
- **Quantum subroutine:** Qiskit Grover search with an equality-check oracle for target k-mers.
- **Metrics:** oracle queries, circuit depth, hit probability, seed hit rate, reference wall-clock.
- **Data:** synthetic reads and k-mer tables (scripts in `data/`).

## Roadmap
- [ ] Synthetic data generator (`data/make_synth.py`)
- [ ] Classical baselines (`classical/linear_seed.py`, `classical/hash_seed.py`)
- [ ] Quantum Grover seeding (`quantum/grover_seed.py`, `quantum/oracle.py`)
- [ ] Evaluation & plots (`eval/compare.py`, `eval/plots.py`)
- [ ] Short write-up

⚠️ This repository is a proof-of-concept / work-in-progress. Not intended as a production-ready aligner.

## Reproduction
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python data/make_synth.py --n_kmers 1024 --k 15
python classical/linear_seed.py --query q.fa --db db_kmers.txt
python classical/hash_seed.py   --query q.fa --db db_kmers.txt
python quantum/grover_seed.py  --query q.fa --db db_kmers.txt --shots 2048
python eval/compare.py --runs runs/

**Licensed under the MIT License – see [LICENSE](./LICENSE).**
