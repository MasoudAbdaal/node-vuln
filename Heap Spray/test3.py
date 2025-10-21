import ctypes
import sys

print("=== 🎯 Heap Spray Demo in Python ===")

def heap_spray_demo():
    # Step 1: Define the shellcode pattern
    # In real exploits, this would be actual shellcode
    nop_sled = b"\x90" * 100  # NOP sled
    shellcode_pattern = b"SHELLCODE_" * 50  # Simulated shellcode
    spray_pattern = nop_sled + shellcode_pattern
    
    print(f"🔹 Spray pattern size: {len(spray_pattern)} bytes")
    print(f"🔹 NOP sled: 100 bytes")
    print(f"🔹 Shellcode pattern: {len(shellcode_pattern)} bytes")
    
    # Step 2: Perform heap spraying
    print("\n🔹 Step 1: Starting Heap Spray...")
    
    spray_objects = []
    spray_count = 1000  # Number of spray allocations
    
    for i in range(spray_count):
        # Create a byte array with our pattern
        sprayed_data = bytearray(spray_pattern)
        spray_objects.append(sprayed_data)
        
        if i % 200 == 0:
            print(f"  🚀 Sprayed {i}/{spray_count} objects...")
    
    print(f"✅ Heap spray completed: {len(spray_objects)} objects")
    
    # Step 3: Show memory statistics
    print("\n🔹 Memory Statistics:")
    total_sprayed = len(spray_objects) * len(spray_pattern)
    print(f"  📊 Total memory sprayed: {total_sprayed:,} bytes")
    print(f"  📊 Approx: {total_sprayed / (1024*1024):.2f} MB")
    
    # Step 4: Demonstrate finding our pattern in memory
    print("\n🔹 Searching for spray pattern in memory...")
    
    # Check if we can find our pattern in the sprayed objects
    found_count = 0
    for i, obj in enumerate(spray_objects[:10]):  # Check first 10
        if spray_pattern in bytes(obj):
            found_count += 1
            if found_count <= 3:
                print(f"  ✅ Pattern found in object {i}")
    
    print(f"  📊 Pattern found in {found_count}/10 sampled objects")
    
    # Step 5: Simulate exploitation attempt
    print("\n🔹 Simulating exploitation...")
    
    # Create a vulnerable scenario
    class VulnerableObject:
        def __init__(self):
            self.buffer = None
            self.size = 0
    
    # Simulate a use-after-free scenario
    vuln_obj = VulnerableObject()
    vuln_obj.buffer = bytearray(100)
    original_buffer = vuln_obj.buffer
    
    print(f"  📍 Original buffer address: {id(original_buffer)}")
    
    # Free the object (simulate UAF)
    del vuln_obj.buffer
    print("  🗑️  Buffer freed (UAF condition created)")
    
    # Now if we allocate new objects, they might land in the freed memory
    new_objects = []
    for i in range(10):
        new_obj = bytearray(100)
        new_objects.append(new_obj)
        if id(new_obj) == id(original_buffer):
            print(f"  🎯 NEW object landed at original buffer address!")
            break
    
    return spray_objects

def advanced_heap_spray():
    print("\n" + "="*50)
    print("=== 🔥 Advanced Heap Spray with Multiple Patterns ===")
    
    # Different spray patterns for different scenarios
    patterns = {
        "rop_chain": b"ROP" * 1000,
        "shellcode_x86": b"\x90" * 500 + b"SC_x86" * 200,
        "shellcode_x64": b"\x90" * 500 + b"SC_x64" * 200,
        "vtable_hijack": b"VTABLE" * 800
    }
    
    sprayed_data = {}
    
    for name, pattern in patterns.items():
        print(f"\n🔹 Spraying {name} pattern ({len(pattern)} bytes)...")
        
        objects = []
        for i in range(200):  # Spray 200 of each
            obj = bytearray(pattern)
            objects.append(obj)
        
        sprayed_data[name] = objects
        print(f"  ✅ {len(objects)} {name} objects sprayed")
    
    # Calculate statistics
    total_memory = 0
    for name, objects in sprayed_data.items():
        pattern_size = len(objects[0]) if objects else 0
        total_memory += len(objects) * pattern_size
    
    print(f"\n📊 Total advanced spray: {total_memory:,} bytes ({total_memory/(1024*1024):.2f} MB)")
    
    return sprayed_data

if __name__ == "__main__":
    # Run basic heap spray
    basic_spray = heap_spray_demo()
    
    # Run advanced heap spray
    advanced_spray = advanced_heap_spray()
    
    print("\n" + "="*50)
    print("=== 🎯 Heap Spray Complete ===")
    print("💡 Keep the references to prevent garbage collection:")
    print(f"   - Basic spray: {len(basic_spray)} objects")
    
    total_advanced = sum(len(obj_list) for obj_list in advanced_spray.values())
    print(f"   - Advanced spray: {total_advanced} objects")
    
    print("\n🔹 The heap is now filled with our spray patterns!")
    print("🔹 In a real exploit, we would now trigger the vulnerability")
    print("🔹 and hope to land in one of our sprayed memory regions.")
    
    # Keep references to prevent GC
    input("\nPress Enter to exit and release memory...")