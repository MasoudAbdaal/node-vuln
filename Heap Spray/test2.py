# heap_spray_simulation_safe.py
# Safe educational simulation of the logic behind "spray" + use-after-free (UAF) effect.
# This does NOT perform memory corruption or write to raw addresses.
# It only demonstrates, at a high level, how a dangling reference might end up
# referring to attacker-controlled data after a spray.

import gc
from collections import Counter

def make_obj(label, size=64, fill=b'X'):
    """Create a bytearray object with an identifying prefix (for clarity)."""
    data = bytearray(fill * (size // len(fill)))
    # embed a small readable tag at start so printed content is clear
    tag = label.encode('ascii')[:8]
    data[:len(tag)] = tag
    return data

def print_sample(ids, objs, note=""):
    print(note)
    for i in range(min(6, len(ids))):
        print(f"  slot[{i}] id={hex(ids[i])} tag={bytes(objs[i][:8])}")

def safe_simulation(total=20, free_indices=None, spray_count=5):
    if free_indices is None:
        free_indices = [2, 5, 7]  # indices we'll "free" to create holes

    # Stage 1: create initial objects (victim objects)
    slots = [make_obj(f"V{i}", size=64, fill=b'V') for i in range(total)]
    before_ids = [id(o) for o in slots]
    print_sample(before_ids, slots, note="Initial slots (victims):")

    # Suppose some external code kept a "dangling reference" to slot 5 (simulated)
    # We simulate a dangling reference simply as the numeric index that used to hold the object.
    dangling_index = 5
    print(f"\n--> We simulate a 'dangling pointer' that refers to slot index {dangling_index} (the victim).")

    # Stage 2: 'free' selected slots by setting them to None (create holes)
    for i in sorted(free_indices):
        print(f"Freeing slot {i} (was id {hex(id(slots[i]))})")
        slots[i] = None

    # encourage GC (no raw-address reuse is forced; this is best-effort)
    # gc.collect()

    # Stage 3: attacker does a spray: allocate many controlled objects hoping to occupy freed slots
    spray_objs = [make_obj(f"S{j}", size=64, fill=b'S') for j in range(spray_count)]
    # place sprayed objects into the first available None slots if any (simple simulation of reuse)
    placed = 0
    for idx in range(len(slots)):
        if slots[idx] is None and placed < len(spray_objs):
            slots[idx] = spray_objs[placed]
            placed += 1

    # Stage 4: observe what the dangling_index now "points to"
    print("\nAfter spray, sample slots (first 10):")
    current_ids = [id(o) if o is not None else None for o in slots]
    for i in range(min(10, len(slots))):
        tag = bytes(slots[i][:8]) if slots[i] is not None else b'<None>'
        print(f"  slot[{i}] id={hex(current_ids[i]) if current_ids[i] else None} tag={tag}")

    # In a real UAF, the dangling pointer would still contain the old raw address.
    # Here we simulate the effect by reading the slot at dangling_index:
    pointed = slots[dangling_index]
    print(f"\nDangling index {dangling_index} now refers to slot content tag: {bytes(pointed[:8]) if pointed is not None else b'<None>'}")

    # Summary: which freed slots were filled by spray objects?
    filled = []
    for i in free_indices:
        filled.append((i, slots[i][:8] if slots[i] is not None else None))
    print("\nSummary of freed slots after spray:")
    for idx, tag in filled:
        print(f"  freed slot {idx} -> now tag: {tag}")

    return {
        "initial_ids": before_ids,
        "final_ids": current_ids,
        "slots": slots,
        "dangling_index": dangling_index
    }

if __name__ == "__main__":
    safe_simulation(total=20, free_indices=[2,5,7], spray_count=5)
