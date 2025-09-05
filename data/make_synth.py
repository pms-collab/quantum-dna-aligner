#!/usr/bin/env python3
import argparse, random, pathlib

NUCS = ["A","C","G","T"]

def rand_dna(n:int)->str:
    return "".join(random.choice(NUCS) for _ in range(n))

def kmers(seq:str, k:int):
    for i in range(len(seq)-k+1):
        yield i, seq[i:i+k]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n_kmers", type=int, default=1024, help="size of k-mer DB (approx)")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--out_db", default="db_kmers.txt")
    ap.add_argument("--out_query", default="q.fa")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    random.seed(args.seed)

    # 대충 n_kmers가 나오도록 참조 길이 설정
    ref_len = args.n_kmers + args.k
    ref = rand_dna(ref_len)

    # DB 저장: "kmer ruindex" 형식
    db_path = pathlib.Path(args.out_db)
    with db_path.open("w") as f:
        for i, kmer in kmers(ref, args.k):
            f.write(f"{kmer}\t{i}\n")

    # 쿼리 하나: DB에 존재하는 k-mer 중 하나를 뽑아 저장
    hit_pos = random.randrange(0, ref_len - args.k + 1)
    query = ref[hit_pos:hit_pos+args.k]
    with open(args.out_query, "w") as f:
        f.write(f">q\n{query}\n")

    print(f"[make_synth] Wrote {db_path} and {args.out_query}; query k-mer = {query} (pos={hit_pos})")

if __name__ == "__main__":
    main()
