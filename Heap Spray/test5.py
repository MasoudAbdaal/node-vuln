#!/usr/bin/env python3
"""
heap_spray_sim.py

Educational simulation of "heap spray": allocate many objects filled with a controllable
pattern and inspect their memory addresses and low-bit distribution.

This is for learning and research only. It does NOT perform or instruct on real-world
exploitation against other software.
"""

import argparse
import gc
from collections import Counter, defaultdict

# helper: printable hex address
def addr(obj):
    return id(obj)

def hex_addr(obj_id):
    return hex(obj_id)

def make_pattern(size, pattern_bytes):
    # repeat the pattern to fill `size` bytes
    if not pattern_bytes:
        return bytearray(size)
    rep = (pattern_bytes * ((size // len(pattern_bytes)) + 1))[:size]
    return bytearray(rep)

def spray(total, size, pattern, noise_before=0, noise_after=0):
    """
    Allocate `noise_before` filler objects, then `total` sprayed objects of `size`
    filled with `pattern`, then `noise_after` filler objects.
    Return list of sprayed objects and their ids.
    """
    # optional noise before spray
    noise1 = [bytearray(8) for _ in range(noise_before)]

    sprayed = []
    for _ in range(total):
        sprayed.append(make_pattern(size, pattern))

    noise2 = [bytearray(8) for _ in range(noise_after)]

    # return sprayed objects and optionally keep noise lists in scope by returning them too
    return sprayed, noise1, noise2

def analyze_addresses(sprayed, page_size=0x1000, show_top=10):
    ids = [addr(o) for o in sprayed]
    unique = len(set(ids))
    total = len(ids)
    print(f"\nAllocated sprayed objects: {total}")
    print(f"Unique addresses among sprayed objects: {unique}")

    # distribution of addresses modulo page_size (low bits)
    lowbits = [i % page_size for i in ids]
    low_counter = Counter(lowbits)
    top_low = low_counter.most_common(show_top)

    print(f"\nTop {show_top} most common low-address (mod {hex(page_size)}) values:")
    for val, cnt in top_low:
        print(f"  low=0x{val:03x}  count={cnt}")

    # bucket by higher-order pages: id // page_size
    pages = [i // page_size for i in ids]
    page_counter = Counter(pages)
    most_common_pages = page_counter.most_common(show_top)
    print(f"\nTop {show_top} pages (page size {hex(page_size)}):")
    for p, cnt in most_common_pages:
        print(f"  page=0x{p:x}  count={cnt}")

    # show any exact-address duplicates (unlikely in CPython)
    dup_map = defaultdict(list)
    for i, oid in enumerate(ids):
        dup_map[oid].append(i)
    duplicates = {k:v for k,v in dup_map.items() if len(v) > 1}
    if duplicates:
        print("\nExact-address duplicates found (object indices sharing same id):")
        for k,v in duplicates.items():
            print(f"  {hex(k)} -> indices {v}")
    else:
        print("\nNo exact-address duplicates found among sprayed objects (expected).")

    return {
        "ids": ids,
        "lowbits_counter": low_counter,
        "page_counter": page_counter,
        "duplicates": duplicates,
    }

def main():
    parser = argparse.ArgumentParser(description="Educational Heap Spray simulation (Python).")
    parser.add_argument("--total", type=int, default=2000, help="Number of sprayed objects to allocate")
    parser.add_argument("--size", type=int, default=1024, help="Size (bytes) of each sprayed object")
    parser.add_argument("--pattern", type=str, default="ABCD", help="Pattern (string) to fill objects with")
    parser.add_argument("--noise-before (NOP Sled)", type=int, default=100, help="Number of small noise allocations before spray")
    parser.add_argument("--noise-after (NOP Sled)", type=int, default=100, help="Number of small noise allocations after spray")
    parser.add_argument("--page-size", type=lambda x: int(x,0), default=0x1000, help="Page size for low-bit analysis (hex ok, default 0x1000)")
    args = parser.parse_args()

    pattern_bytes = args.pattern.encode("utf-8")

    print("=== Heap Spray Simulation ===")
    print(f"Total spray objects: {args.total}, size each: {args.size} bytes, pattern: {args.pattern!r}")
    print(f"Noise before: {args.noise_before}, noise after: {args.noise_after}")
    print("For research/education only — not an exploit.")

    # encourage a clean start
    gc.collect()

    sprayed, noise1, noise2 = spray(args.total, args.size, pattern_bytes, args.noise_before, args.noise_after)

    # optionally do some accesses to keep Python from optimizing or freeing early
    # e.g., touch first and last byte
    for o in sprayed[:10]:
        _ = o[0]
    for o in sprayed[-10:]:
        _ = o[-1]

    # analyze
    result = analyze_addresses(sprayed, page_size=args.page_size, show_top=8)

    print("\nDone. You can tweak --total, --size, --pattern and noise counts to observe different behaviors.")

if __name__ == "__main__":
    main()
