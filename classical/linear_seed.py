#!/usr/bin/env python3
import argparse, time

def load_db(path):
    db=[]
    with open(path) as f:
        for line in f:
            k, pos = line.strip().split("\t")
            db.append((k,int(pos)))
    return db

def load_query(path):
    with open(path) as f:
        lines=[l.strip() for l in f if l.strip() and not l.startswith(">")]
    return lines[0]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--db", required=True)
    args=ap.parse_args()

    q = load_query(args.query)
    db = load_db(args.db)

    t0=time.time()
    hits=[(k,pos) for k,pos in db if k==q]
    dt=time.time()-t0

    print(f"[linear] query={q} hits={len(hits)} time_sec={dt:.6f}")
    if hits[:10]:  # 앞쪽 몇 개만 표시
        print("[linear] first_hits:", hits[:10])

if __name__=="__main__":
    main()

