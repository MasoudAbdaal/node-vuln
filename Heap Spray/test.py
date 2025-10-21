# heap_spray_minimal.py
# Minimal, educational demonstration of "heap spray" effect in CPython.
# Comments and code intentionally simple — not an exploit.

import gc
from collections import Counter

def make_pattern(size, pattern=b'A'):
    rep = (pattern * ((size // len(pattern)) + 1))[:size]
    return bytearray(rep)

def simple_spray(total=200, size=256, pattern=b'AB'):
    # try to start from a relatively clean state
    # gc.collect()

    sprayed = [make_pattern(size, pattern) for _ in range(total)]

    # capture numeric ids (addresses in CPython terms)
    ids = [id(o) for o in sprayed]

    # print a few sample addresses
    print("Sample addresses (first 10):")
    for i, a in enumerate(ids[:10]):
        print(f"  [{i:2}] {hex(a)}")

    # basic stats
    print(f"\nTotal sprayed objects: {len(ids)}")
    print(f"Unique addresses: {len(set(ids))}")

    # look at low bits distribution (page-like)
    page = 0x1000
    lowbits = [x % page for x in ids]
    counter = Counter(lowbits)
    most_common = counter.most_common(8)
    print(f"\nTop low-bit offsets modulo {hex(page)}:")
    for off, cnt in most_common:
        print(f"  offset 0x{off:03x} -> {cnt} objects")

    # show first/mid/last addresses for quick visual
    print("\nFirst / Middle / Last addresses:")
    print(" ", hex(ids[0]), "/", hex(ids[len(ids)//2]), "/", hex(ids[-1]))

    return ids, counter

if __name__ == "__main__":
    # tweak these to observe different allocator behavior
    simple_spray(total=600, size=512, pattern=b'QW')
