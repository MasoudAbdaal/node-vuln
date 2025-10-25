const express = require('express');
const { VM } = require('vm2');
const path = require('path');
const cors = require('cors');
const fs = require('fs');

const app = express();
const port = 3000;

// Middleware
app.use(express.json());
app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('.'));

// Vulnerable vm2 instance (version 3.9.19)
const vm = new VM({
    timeout: 5000,
    sandbox: {
        console: console,
        // Intentionally allowing some globals that could be exploited
        Buffer: Buffer,
        process: process
    }
});

// Vulnerable endpoint - executes user code in vm2 sandbox
app.post('/execute', (req, res) => {
    try {
        const userCode = req.body.code;
        
        if (!userCode) {
            return res.status(400).json({ 
                error: 'No code provided',
                message: 'Please provide JavaScript code to execute'
            });
        }

        console.log(`[VULNERABLE] Executing user code: ${userCode.substring(0, 100)}...`);
        
        // This is the vulnerable part - executing user code in vm2 sandbox
        const result = vm.run(userCode);
        
        res.json({
            success: true,
            result: result,
            message: 'Code executed successfully in sandbox'
        });
        
    } catch (error) {
        console.error(`[ERROR] Sandbox execution failed:`, error.message);
        res.status(500).json({
            error: 'Execution failed',
            message: error.message,
            type: error.constructor.name
        });
    }
});

// Test endpoint to verify sandbox escape
app.get('/test-escape', (_, res) => {
    // Server error: TypeError: require(...).createContext(...).Script is not a function
    // const escapeMethod1 =  require('vm').createContext().Script(`this.constructor.constructor("return process.pid")()`).runInContext()
    
    const escapeMethod1 = new (require('vm').Script)(`this.constructor.constructor("return process.platform")()`).runInThisContext();
    
    res.json({
        message: 'If you can see this, sandbox escape was successful!',
        timestamp: new Date().toISOString(),
        process: {
            pid: process.pid,
            platform: process.platform,
            version: process.version
        }
    });
});

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'running',
        vm2_version: require('vm2/package.json').version,
        node_version: process.version,
        timestamp: new Date().toISOString()
    });
});

// Root endpoint
app.get('/', (_, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Error handling
app.use((err, _, res, resp) => {
    console.error('Server error:', err);
    res.status(500).json({
        error: 'Internal server error',
        message: err.message
    });
});

app.listen(port, () => {
    console.log(`Server: http://localhost:${port}`);
    console.log(`VM2 Version: ${require('vm2/package.json').version}`);
    console.log(`Node Version: ${process.version}`);
});
