const express = require('express');
const cors = require('cors');
const fileUpload = require('express-fileupload');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(cors());
app.use(fileUpload());

// 🚨 آسیب‌پذیری: آپلود فایل با قابلیت Path Traversal
app.post('/upload', (req, res) => {
    if (!req.files || !req.files.file) {
        return res.status(400).send('No file uploaded');
    }

    const file = req.files.file;
    const fileName = req.body.filename || file.name; // 🚨 ورودی کاربر بدون اعتبارسنجی
    
    // 🚨 آسیب‌پذیری اصلی: عدم اعتبارسنجی مسیر
    const uploadPath = path.join(__dirname, 'uploads', fileName);
    
    file.mv(uploadPath, (err) => {
        if (err) {
            return res.status(500).send(err);
        }
        res.send(`File uploaded to: ${uploadPath}`);
    });
});

// 🚨 آسیب‌پذیری: خواندن فایل‌های حساس
app.get('/files', (req, res) => {
    const filePath = req.query.path; // 🚨 ورودی مستقیم از کاربر
    const fullPath = path.join(__dirname, filePath);
    
    fs.readFile(fullPath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).send('Error reading file');
        }
        res.send(data);
    });
});

app.listen(3000, () => {
    console.log('Vulnerable Express server running on port 3000');
});