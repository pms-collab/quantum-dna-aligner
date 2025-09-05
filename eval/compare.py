#!/usr/bin/env python3
import argparse, json, time, subprocess

def run(cmd):
    t0=time.time()
    p=subprocess.run(cmd, shell=True, capture_output=True, text=True)
    dt=time.time()-t0
    return dt, p.stdout.strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs/")
    ap.add_argument("--query", default="q.fa")
    ap.add_argument("--db", default="db_kmers.txt")
    args=ap.parse_args()

    res={}
    dt, out = run(f"python classical/linear_seed.py --query {args.query} --db {args.db}")
    res["linear"]={"time_sec":dt,"stdout":out}

    dt, out = run(f"python classical/hash_seed.py --query {args.query} --db {args.db}")
    res["hash"]={"time_sec":dt,"stdout":out}

    dt, out = run(f"python quantum/grover_seed.py --query {args.query} --db {args.db} --shots 1024")
    res["grover"]={"time_sec":dt,"stdout":out}

    print(json.dumps(res, indent=2))

if __name__=="__main__":
    main()

