import gc
import random

# helper: printable hex address for an object
def addr(obj):
    return hex(id(obj)) if obj is not None else "<None>"

def heap_feng_shui_check(total=12, indices_to_free=None, new_alloc_count=None, size=64):

    if indices_to_free is None:
        indices_to_free = [10, 8, 5, 3, 4, 1]
    if new_alloc_count is None:
        new_alloc_count = len(indices_to_free)

    # Stage 1: create objects and record addresses
    A = [bytearray(size) for _ in range(total)]
    before_ids = [id(x) for x in A]

    print("=== Stage 1: initial addresses ===")
    for i, x in enumerate(A):
        print(f"A[{i}] -> {addr(x)}")

    # Stage 2: 'free' selected indices by replacing with None (Or del A[]) (preserve list indices)
    print("\n=== Stage 2: freeing selected indices ===")
    freed_ids = []
    for i in indices_to_free:
        freed_ids.append(before_ids[i])
        A[i] = None  # With None
        # del A[i]   # With del A[]
        print(f"freed A[{i}] (was {hex(before_ids[i])})")

    # gc.collect() reset the allocation address range!
    gc.collect()

    # Stage 3: allocate new objects
    print("\n=== Stage 3: allocating new objects ===")
    # allocate some extra noise objects first (optional, can influence allocator)
    noise = [bytearray(size) for _ in range(random.randint(0, 5))]

    new_objs = [bytearray(size) for _ in range(new_alloc_count)]
    new_ids = [id(x) for x in new_objs]

    for j, nid in enumerate(new_ids):
        print(f"new_obj[{j}] -> {hex(nid)}")

    # Stage 4: compare freed_ids vs new_ids
    print("\n=== Results: reused addresses ===")
    freed_set = set(freed_ids)
    reused_map = {}  # freed_id -> list of new_ids that reused it
    for fid in freed_ids:
        reused_map[fid] = []

    for nid in new_ids:
        if nid in freed_set:
            reused_map[nid].append(nid)

    any_reused = False
    for fid, hits in reused_map.items():
        if hits:
            any_reused = True
            print(f"FREED {hex(fid)} was reused by new object(s): {[hex(x) for x in hits]}")
        else:
            print(f"FREED {hex(fid)} was NOT reused")

    print("\nSummary:")
    print(f"Total freed slots: {len(freed_ids)}")
    print(f"Total new allocations checked: {len(new_ids)}")
    print("Any reused:", any_reused)

    # return structures in case caller wants to inspect programmatically
    return {
        "before_ids": before_ids,
        "freed_ids": freed_ids,
        "new_ids": new_ids,
        "reused_map": reused_map,
        "any_reused": any_reused,
    }

if __name__ == "__main__":
    result = heap_feng_shui_check()
