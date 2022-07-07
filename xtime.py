#!/usr/bin/env python3

import argparse
import subprocess
import time
import sys
import random

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--times", type=int, default=10)
    p.add_argument("command", nargs='*')
    return p.parse_args()

def bootstrap(data, times=1000, interval=0.95):
    samples = []
    ldata = len(data)
    for _ in range(times):
        sampled = []
        for num in range(ldata):
            sampled.append(data[random.randrange(ldata)])
        samples.append(sum(sampled) / ldata)
    samples.sort()
    remain = (1.0 - interval) / 2
    bot_idx = int(times * remain)
    top_idx = int(times * (1.0 - remain))
    return samples[bot_idx], samples[top_idx]



def execute(command, nrun, total):
    start = time.monotonic()
    rcode = subprocess.call(command)
    end = time.monotonic()
    dur = end - start
    cmdstring = " ".join(command)
    if len(cmdstring) > 23:
        cmdstring = cmdstring[:20] + "..."
    print(f"{rcode} <- [{dur:.2F}s] ({nrun + 1}/{total}) {cmdstring}", file=sys.stderr)
    return dur

def main(args):
    times = []
    for i in range(args.times):
        exec_time = execute(args.command, i, args.times)
        times.append(exec_time)

    times.sort()

    avg_time = sum(times) / len(times)
    all_times_str = ",".join(format(x, ".2F") for x in times)
    time_ci_bot, time_ci_top = bootstrap(times)
    print(f"{avg_time:.2F} ({time_ci_bot:.2F}, {time_ci_top:.2F})\t{all_times_str}\n")



if __name__ == "__main__":
    main(parse_args())