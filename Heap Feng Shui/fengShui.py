import ctypes
import gc

# helper function to get the exact memory address in CPython
def addr(obj):
    return hex(id(obj))

print("=== Stage 1: initial object creation ===")
A = [bytearray(32) for _ in range(10)]
for i, a in enumerate(A):
    print(f"A[{i}] -> {addr(a)}")

print("\n=== Stage 2: freeing some objects ===")
print("\nObjects will shifted after freeing!")
del A[9]
del A[5]
del A[3]
del A[4]

# if gc.collect() is called, the allocation addres will changed and will not be reused
# gc.collect()

B = bytearray(32)
C = bytearray(32)

print(f"B -> {addr(B)}")
print(f"C -> {addr(C)}")

print("\n=== Stage 3: checking reuse of addresses ===")
D = bytearray(32)
E = bytearray(32)
print(f"D -> {addr(D)}")
print(f"E -> {addr(E)}")

print("\nFinished ✅")
