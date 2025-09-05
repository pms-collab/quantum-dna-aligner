#!/usr/bin/env python3
import argparse, time
from collections import defaultdict

def load_db_map(path):
    mp=defaultdict(list)
    with open(path) as f:
        for line in f:
            k, pos = line.strip().split("\t")
            mp[k].append(int(pos))
    return mp

def load_query(path):
    with open(path) as f:
        for line in f:
            if line.startswith(">"): continue
            l=line.strip()
            if l: return l

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--db", required=True)
    args=ap.parse_args()

    q = load_query(args.query)
    t0=time.time()
    mp = load_db_map(args.db)
    build=time.time()-t0

    t1=time.time()
    hits = mp.get(q, [])
    lookup=time.time()-t1

    print(f"[hash] query={q} hits={len(hits)} build_sec={build:.6f} lookup_sec={lookup:.6f}")
    if hits[:10]:
        print("[hash] first_hits:", hits[:10])

if __name__=="__main__":
    main()

