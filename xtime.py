#!/usr/bin/env python3

import argparse
import subprocess
import time
import sys

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--times", type=int, default=10)
    p.add_argument("command", nargs='*')
    return p.parse_args()


def execute(command, nrun, total):
    start = time.monotonic()
    rcode = subprocess.call(command)
    end = time.monotonic()
    dur = end - start
    cmdstring = " ".join(command)
    if len(cmdstring) > 23:
        cmdstring = cmdstring[:20] + "..."
    print(f"{rcode} <- [{dur:.2F}s] ({nrun}/{total}) {cmdstring}", file=sys.stderr)
    return dur

def main(args):
    times = []
    for i in range(args.times):
        exec_time = execute(args.command, i, args.times)
        times.append(exec_time)

    avg_time = sum(times) / len(times)
    all_times_str = ",".join(format(x, ".2F") for x in times)
    print(f"{avg_time:.2F}\t{all_times_str}\n")



if __name__ == "__main__":
    main(parse_args())