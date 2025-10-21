// heap_spray.js
console.log("=== 🎯 Heap Spray Demo in Node.js ===");

function heapSprayDemo() {
    // Step 1: Define the shellcode pattern
    // In Node.js, we use Buffer instead of bytearray
    const nopSled = Buffer.alloc(100, 0x90); // NOP sled (0x90 = NOP in x86)
    const shellcodePattern = Buffer.from("SHELLCODE_".repeat(50));
    const sprayPattern = Buffer.concat([nopSled, shellcodePattern]);
    
    console.log(`🔹 Spray pattern size: ${sprayPattern.length} bytes`);
    console.log(`🔹 NOP sled: ${nopSled.length} bytes`);
    console.log(`🔹 Shellcode pattern: ${shellcodePattern.length} bytes`);
    
    // Step 2: Perform heap spraying
    console.log("\n🔹 Step 1: Starting Heap Spray...");
    
    const sprayObjects = [];
    const sprayCount = 1000; // Number of spray allocations
    
    for (let i = 0; i < sprayCount; i++) {
        // Create a new Buffer with our pattern
        const sprayedData = Buffer.from(sprayPattern);
        sprayObjects.push(sprayedData);
        
        if (i % 200 === 0) {
            console.log(`  🚀 Sprayed ${i}/${sprayCount} objects...`);
        }
    }
    
    console.log(`✅ Heap spray completed: ${sprayObjects.length} objects`);
    
    // Step 3: Show memory statistics
    console.log("\n🔹 Memory Statistics:");
    const totalSprayed = sprayObjects.length * sprayPattern.length;
    console.log(`  📊 Total memory sprayed: ${totalSprayed.toLocaleString()} bytes`);
    console.log(`  📊 Approx: ${(totalSprayed / (1024 * 1024)).toFixed(2)} MB`);
    
    // Show Node.js memory usage
    const memoryUsage = process.memoryUsage();
    console.log(`  📊 RSS: ${(memoryUsage.rss / (1024 * 1024)).toFixed(2)} MB`);
    console.log(`  📊 Heap Total: ${(memoryUsage.heapTotal / (1024 * 1024)).toFixed(2)} MB`);
    console.log(`  📊 Heap Used: ${(memoryUsage.heapUsed / (1024 * 1024)).toFixed(2)} MB`);
    
    // Step 4: Demonstrate finding our pattern in memory
    console.log("\n🔹 Searching for spray pattern in memory...");
    
    // Check if we can find our pattern in the sprayed objects
    let foundCount = 0;
    for (let i = 0; i < Math.min(10, sprayObjects.length); i++) {
        const obj = sprayObjects[i];
        // Compare buffers to find our pattern
        if (obj.includes(0x90) && obj.includes(0x53)) { // 0x53 = 'S' in ASCII
            foundCount++;
            if (foundCount <= 3) {
                console.log(`  ✅ Pattern found in object ${i}`);
            }
        }
    }
    
    console.log(`  📊 Pattern found in ${foundCount}/10 sampled objects`);
    
    // Step 5: Simulate exploitation attempt
    console.log("\n🔹 Simulating exploitation...");
    
    // Create a vulnerable scenario
    class VulnerableObject {
        constructor() {
            this.buffer = null;
            this.size = 0;
        }
    }
    
    // Simulate a use-after-free scenario
    const vulnObj = new VulnerableObject();
    vulnObj.buffer = Buffer.alloc(100);
    const originalBuffer = vulnObj.buffer;
    
    // In Node.js we can't get direct memory addresses, but we can show object references
    console.log(`  📍 Original buffer reference created`);
    
    // Free the object (simulate UAF)
    vulnObj.buffer = null;
    console.log("  🗑️  Buffer freed (UAF condition created)");
    
    // Now if we allocate new objects, they might land in the freed memory
    const newObjects = [];
    for (let i = 0; i < 10; i++) {
        const newObj = Buffer.alloc(100);
        newObjects.push(newObj);
        // In Node.js we can't compare memory addresses directly
    }
    
    console.log("  🔄 Allocated new objects (potential UAF exploitation)");
    
    return sprayObjects;
}

function advancedHeapSpray() {
    console.log("\n" + "=".repeat(50));
    console.log("=== 🔥 Advanced Heap Spray with Multiple Patterns ===");
    
    // Different spray patterns for different scenarios
    const patterns = {
        "rop_chain": Buffer.from("ROP".repeat(1000)),
        "shellcode_x86": Buffer.concat([
            Buffer.alloc(500, 0x90), 
            Buffer.from("SC_x86".repeat(200))
        ]),
        "shellcode_x64": Buffer.concat([
            Buffer.alloc(500, 0x90),
            Buffer.from("SC_x64".repeat(200))
        ]),
        "vtable_hijack": Buffer.from("VTABLE".repeat(800))
    };
    
    const sprayedData = {};
    
    for (const [name, pattern] of Object.entries(patterns)) {
        console.log(`\n🔹 Spraying ${name} pattern (${pattern.length} bytes)...`);
        
        const objects = [];
        for (let i = 0; i < 200; i++) { // Spray 200 of each
            const obj = Buffer.from(pattern);
            objects.push(obj);
        }
        
        sprayedData[name] = objects;
        console.log(`  ✅ ${objects.length} ${name} objects sprayed`);
    }
    
    // Calculate statistics
    let totalMemory = 0;
    for (const [name, objects] of Object.entries(sprayedData)) {
        const patternSize = objects.length > 0 ? objects[0].length : 0;
        totalMemory += objects.length * patternSize;
    }
    
    console.log(`\n📊 Total advanced spray: ${totalMemory.toLocaleString()} bytes (${(totalMemory/(1024*1024)).toFixed(2)} MB)`);
    
    // Show final memory usage
    const finalMemory = process.memoryUsage();
    console.log(`📊 Final RSS: ${(finalMemory.rss / (1024 * 1024)).toFixed(2)} MB`);
    
    return sprayedData;
}

// Memory monitoring function
function monitorMemory(phase) {
    const memory = process.memoryUsage();
    console.log(`\n📊 Memory at ${phase}:`);
    console.log(`  RSS: ${(memory.rss / (1024 * 1024)).toFixed(2)} MB`);
    console.log(`  Heap Total: ${(memory.heapTotal / (1024 * 1024)).toFixed(2)} MB`);
    console.log(`  Heap Used: ${(memory.heapUsed / (1024 * 1024)).toFixed(2)} MB`);
    console.log(`  External: ${(memory.external / (1024 * 1024)).toFixed(2)} MB`);
}

// Main execution
if (require.main === module) {
    monitorMemory("start");
    
    // Run basic heap spray
    const basicSpray = heapSprayDemo();
    
    monitorMemory("after basic spray");
    
    // Run advanced heap spray
    const advancedSpray = advancedHeapSpray();
    
    monitorMemory("after advanced spray");
    
    console.log("\n" + "=".repeat(50));
    console.log("=== 🎯 Heap Spray Complete ===");
    console.log("💡 Keep the references to prevent garbage collection:");
    console.log(`   - Basic spray: ${basicSpray.length} objects`);
    
    const totalAdvanced = Object.values(advancedSpray).reduce((sum, arr) => sum + arr.length, 0);
    console.log(`   - Advanced spray: ${totalAdvanced} objects`);
    
    console.log("\n🔹 The heap is now filled with our spray patterns!");
    console.log("🔹 In a real exploit, we would now trigger the vulnerability");
    console.log("🔹 and hope to land in one of our sprayed memory regions.");
    
    // Keep references to prevent GC and wait for user input
    console.log("\n💾 References kept alive. Process will stay running...");
    console.log("Press Ctrl+C to exit and release memory");
    
    // Keep the process alive and references active
    setInterval(() => {
        // This keeps the event loop running and references alive
    }, 1000);
}

module.exports = { heapSprayDemo, advancedHeapSpray, monitorMemory };