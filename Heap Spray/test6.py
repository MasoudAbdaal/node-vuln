# refined_heap_spray_uaf_sim.py
# Educational simulation of heap spray + UAF. Safe; no raw memory access.
# Demonstrates how sprayed patterns might fill freed slots in a real exploit.

import gc
from collections import Counter

def make_obj(label, size=64, fill=b'X'):
    """Create a bytearray with tag for identification."""
    data = bytearray(fill * (size // len(fill)))
    tag = label.encode('ascii')[:8]
    data[:len(tag)] = tag
    return data

def print_sample(ids, objs, note=""):
    print(note)
    for i in range(min(6, len(ids))):
        print(f"  slot[{i}] id={hex(ids[i])} tag={bytes(objs[i][:8])}")

def refined_simulation(total=20, free_indices=[2, 5, 7], spray_count=5):
    # Stage 1: Initial allocations (victims)
    slots = [make_obj(f"V{i}", size=64, fill=b'V') for i in range(total)]
    before_ids = [id(o) for o in slots]
    print_sample(before_ids, slots, note="Initial slots (victims):")

    # Simulate dangling pointer (UAF) to slot 5
    dangling_index = 5
    print(f"\n--> Simulating UAF: Dangling reference to slot {dangling_index}.")

    # Stage 2: Free slots to create holes
    for i in sorted(free_indices):
        print(f"Freeing slot {i} (id {hex(id(slots[i]))})")
        slots[i] = None

    # gc.collect()  # Encourage reuse (best-effort in Python)

    # Stage 3: Heap spray with NOP sled + shellcode pattern
    nop_sled = b'\x90' * 32  # Real-world NOP for sliding
    shellcode = b'SHELLCODE' * 4  # Simulated payload
    spray_pattern = nop_sled + shellcode
    spray_objs = [bytearray(spray_pattern * (64 // len(spray_pattern) + 1))[:64] for _ in range(spray_count)]

    # Place spray into holes (simulate memory reuse)
    placed = 0
    for idx in range(len(slots)):
        if slots[idx] is None and placed < len(spray_objs):
            slots[idx] = spray_objs[placed]
            placed += 1

    # Stage 4: Observe UAF effect
    print("\nAfter spray, sample slots:")
    current_ids = [id(o) if o is not None else None for o in slots]
    for i in range(min(10, len(slots))):
        tag = bytes(slots[i][:8]) if slots[i] is not None else b'<None>'
        print(f"  slot[{i}] id={hex(current_ids[i]) if current_ids[i] else None} tag={tag}")

    # Dangling access simulation
    pointed = slots[dangling_index]
    print(f"\nUAF: Dangling now points to tag: {bytes(pointed[:8]) if pointed else b'<None>'}")

    # Address analysis (real-world: check clustering despite ASLR)
    low_bits = [cid % 0x1000 for cid in current_ids if cid]
    counter = Counter(low_bits)
    print("\nLow-bit distribution (mod 0x1000):", counter.most_common(5))

if __name__ == "__main__":
    refined_simulation()