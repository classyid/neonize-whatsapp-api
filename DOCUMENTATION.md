# 📱 WhatsApp API - Complete Documentation

## 🚀 Overview

**WhatsApp API** adalah REST API lengkap untuk mengirim berbagai jenis pesan WhatsApp termasuk text, gambar, dokumen, audio, video, dan sticker. API ini dibangun menggunakan Flask dan library Neonize untuk integrasi dengan WhatsApp Web.

### ⚡ Quick Info
- **Base URL**: `http://your-server:5000`
- **Version**: 2.0.0
- **Protocol**: HTTP/HTTPS
- **Format**: JSON
- **Authentication**: None (dapat ditambahkan)

---

## 📋 Table of Contents

1. [API Endpoints](#api-endpoints)
2. [Request/Response Format](#requestresponse-format)
3. [Supported Media Types](#supported-media-types)
4. [Error Handling](#error-handling)
5. [Examples](#examples)
6. [Rate Limits](#rate-limits)
7. [Troubleshooting](#troubleshooting)

---

## 🔗 API Endpoints

### 1. **Health Check**
Get API status and supported features.

```http
GET /
```

**Response:**
```json
{
  "service": "WhatsApp API - Complete Media Support",
  "status": "running",
  "bot_connected": true,
  "version": "2.0.0",
  "features": {
    "text_messages": "✅ Working",
    "image_messages": "✅ Working", 
    "document_messages": "✅ Working",
    "audio_messages": "✅ Available",
    "video_messages": "✅ Available",
    "sticker_messages": "✅ Available"
  },
  "supported_formats": {
    "images": ["jpg", "jpeg", "png", "gif", "webp"],
    "documents": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "zip", "rar", "7z"],
    "audio": ["mp3", "wav", "ogg", "m4a", "aac", "flac"],
    "video": ["mp4", "avi", "mov", "mkv", "webm", "3gp", "flv"],
    "stickers": ["webp"]
  },
  "file_size_limits": {
    "images": "16MB",
    "documents": "32MB",
    "audio": "16MB",
    "video": "64MB",
    "stickers": "1MB"
  },
  "endpoints": [
    "POST /api/send-message - Send text message",
    "POST /api/send-image - Send image with caption",
    "POST /api/send-document - Send document with caption",
    "POST /api/send-audio - Send audio file",
    "POST /api/send-video - Send video with caption",
    "POST /api/send-sticker - Send WebP sticker",
    "GET /api/status - Bot status"
  ]
}
```

### 2. **Bot Status**
Check WhatsApp bot connection status.

```http
GET /api/status
```

**Response:**
```json
{
  "bot_connected": true,
  "thread_alive": true,
  "upload_folder": "uploads",
  "supported_formats": {
    "images": ["jpg", "jpeg", "png", "gif", "webp"],
    "documents": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "zip", "rar", "7z"],
    "audio": ["mp3", "wav", "ogg", "m4a", "aac", "flac"],
    "video": ["mp4", "avi", "mov", "mkv", "webm", "3gp", "flv"],
    "stickers": ["webp"]
  },
  "file_size_limits": {
    "images": "16MB",
    "documents": "32MB",
    "audio": "16MB",
    "video": "64MB",
    "stickers": "1MB"
  },
  "message": "Bot status retrieved"
}
```

### 3. **Send Text Message**
Send a text message to WhatsApp number.

```http
POST /api/send-message
```

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "phone": "6281234567890",
  "message": "Hello from WhatsApp API!"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Text message sent successfully",
  "data": {
    "phone": "6281234567890",
    "message": "Hello from WhatsApp API!",
    "type": "text",
    "timestamp": "2025-08-15 17:38:34.475734"
  }
}
```

### 4. **Send Image**
Send an image with optional caption.

```http
POST /api/send-image
```

**Content-Type:** `multipart/form-data`

**Form Parameters:**
- `phone` (required): WhatsApp number
- `file` (required): Image file
- `caption` (optional): Image caption

**Example:**
```bash
curl -X POST http://localhost:5000/api/send-image \
  -F "phone=6281234567890" \
  -F "caption=📸 Beautiful sunset!" \
  -F "file=@image.jpg"
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Image sent successfully",
  "data": {
    "phone": "6281234567890",
    "filename": "sunset.jpg",
    "caption": "📸 Beautiful sunset!",
    "type": "image",
    "file_size_kb": 245.67,
    "timestamp": "2025-08-15 17:38:34.475734"
  }
}
```

### 5. **Send Document**
Send a document with optional caption.

```http
POST /api/send-document
```

**Content-Type:** `multipart/form-data`

**Form Parameters:**
- `phone` (required): WhatsApp number
- `file` (required): Document file
- `caption` (optional): Document caption

**Example:**
```bash
curl -X POST http://localhost:5000/api/send-document \
  -F "phone=6281234567890" \
  -F "caption=📄 Important document" \
  -F "file=@report.pdf"
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Document sent successfully",
  "data": {
    "phone": "6281234567890",
    "filename": "report.pdf",
    "caption": "📄 Important document",
    "type": "document",
    "file_size_kb": 1024.00,
    "timestamp": "2025-08-15 17:38:34.475734"
  }
}
```

### 6. **Send Audio**
Send an audio file.

```http
POST /api/send-audio
```

**Content-Type:** `multipart/form-data`

**Form Parameters:**
- `phone` (required): WhatsApp number
- `file` (required): Audio file

**Example:**
```bash
curl -X POST http://localhost:5000/api/send-audio \
  -F "phone=6281234567890" \
  -F "file=@voice_message.mp3"
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Audio sent successfully",
  "data": {
    "phone": "6281234567890",
    "filename": "voice_message.mp3",
    "type": "audio",
    "file_size_kb": 2869.42,
    "timestamp": "2025-08-15 17:38:54.824421"
  }
}
```

### 7. **Send Video**
Send a video with optional caption.

```http
POST /api/send-video
```

**Content-Type:** `multipart/form-data`

**Form Parameters:**
- `phone` (required): WhatsApp number
- `file` (required): Video file
- `caption` (optional): Video caption

**Example:**
```bash
curl -X POST http://localhost:5000/api/send-video \
  -F "phone=6281234567890" \
  -F "caption=🎬 Amazing video!" \
  -F "file=@demo.mp4"
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Video sent successfully",
  "data": {
    "phone": "6281234567890",
    "filename": "demo.mp4",
    "caption": "🎬 Amazing video!",
    "type": "video",
    "file_size_kb": 34.06,
    "timestamp": "2025-08-15 17:38:34.475734"
  }
}
```

### 8. **Send Sticker**
Send a WebP sticker.

```http
POST /api/send-sticker
```

**Content-Type:** `multipart/form-data`

**Form Parameters:**
- `phone` (required): WhatsApp number
- `file` (required): WebP sticker file

**Example:**
```bash
curl -X POST http://localhost:5000/api/send-sticker \
  -F "phone=6281234567890" \
  -F "file=@funny_sticker.webp"
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Sticker sent successfully",
  "data": {
    "phone": "6281234567890",
    "filename": "funny_sticker.webp",
    "type": "sticker",
    "file_size_kb": 23.45,
    "timestamp": "2025-08-15 17:38:34.475734"
  }
}
```

---

## 📝 Request/Response Format

### Phone Number Format
Phone numbers can be sent in various formats:
- `081234567890` (local format)
- `+6281234567890` (international format)
- `6281234567890` (without +)

The API automatically converts to WhatsApp format: `6281234567890@s.whatsapp.net`

### File Upload Requirements
- **Max file sizes vary by type** (see supported media types)
- **Files are automatically deleted** after sending
- **Secure filename processing** to prevent path traversal
- **MIME type detection** for proper file handling

---

## 🎯 Supported Media Types

| Media Type | Extensions | Max Size | Caption Support | Notes |
|------------|------------|----------|-----------------|-------|
| **Images** | jpg, jpeg, png, gif, webp | 16MB | ✅ Yes | Most common image formats |
| **Documents** | pdf, doc, docx, xls, xlsx, ppt, pptx, txt, zip, rar, 7z | 32MB | ✅ Yes | Office documents and archives |
| **Audio** | mp3, wav, ogg, m4a, aac, flac | 16MB | ❌ No | Voice messages and music |
| **Video** | mp4, avi, mov, mkv, webm, 3gp, flv | 64MB | ✅ Yes | Video files with various codecs |
| **Stickers** | webp | 1MB | ❌ No | WebP format only, small size |

---

## ❌ Error Handling

### Error Response Format
All errors return JSON with consistent format:

```json
{
  "status": "error",
  "message": "Error description here"
}
```

### Common Error Codes

#### 400 - Bad Request
```json
{
  "status": "error",
  "message": "Phone number required"
}
```

```json
{
  "status": "error",
  "message": "Invalid file type. Allowed: ['jpg', 'jpeg', 'png', 'gif', 'webp']"
}
```

```json
{
  "status": "error",
  "message": "File too large. Max size for images: 16MB"
}
```

#### 503 - Service Unavailable
```json
{
  "status": "error",
  "message": "Bot not connected"
}
```

#### 500 - Internal Server Error
```json
{
  "status": "error",
  "message": "Failed to send message"
}
```

### Validation Rules

1. **Phone Number:**
   - Must be 10-15 digits
   - Automatically formatted to Indonesian format (+62)
   - Invalid formats return 400 error

2. **File Validation:**
   - File type checked by extension
   - File size validated per media type
   - Missing files return 400 error

3. **Bot Status:**
   - Must be connected to WhatsApp
   - Returns 503 if not connected

---

## 📖 Examples

### Text Message Example

**JavaScript (fetch):**
```javascript
const response = await fetch('http://localhost:5000/api/send-message', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    phone: '6281234567890',
    message: 'Hello from JavaScript!'
  })
});

const result = await response.json();
console.log(result);
```

**Python (requests):**
```python
import requests

data = {
    "phone": "6281234567890",
    "message": "Hello from Python!"
}

response = requests.post(
    'http://localhost:5000/api/send-message',
    json=data
)

print(response.json())
```

**PHP:**
```php
<?php
$data = array(
    'phone' => '6281234567890',
    'message' => 'Hello from PHP!'
);

$response = file_get_contents(
    'http://localhost:5000/api/send-message',
    false,
    stream_context_create(array(
        'http' => array(
            'method' => 'POST',
            'header' => 'Content-Type: application/json',
            'content' => json_encode($data)
        )
    ))
);

echo $response;
?>
```

### Image Upload Example

**JavaScript (FormData):**
```javascript
const formData = new FormData();
formData.append('phone', '6281234567890');
formData.append('caption', '📸 Image from JavaScript');
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:5000/api/send-image', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result);
```

**Python (requests with files):**
```python
import requests

files = {'file': open('image.jpg', 'rb')}
data = {
    'phone': '6281234567890',
    'caption': '📸 Image from Python'
}

response = requests.post(
    'http://localhost:5000/api/send-image',
    files=files,
    data=data
)

print(response.json())
```

### Complete Test Script

**Python test script:**
```python
import requests
import json

API_BASE = "http://localhost:5000"
TEST_PHONE = "6281234567890"

def test_all_endpoints():
    # Test text message
    print("Testing text message...")
    response = requests.post(f"{API_BASE}/api/send-message", json={
        "phone": TEST_PHONE,
        "message": "🧪 API Test - All endpoints working!"
    })
    print(f"Text: {response.status_code} - {response.json()}")
    
    # Test image (if you have test.jpg)
    try:
        with open('test.jpg', 'rb') as f:
            response = requests.post(f"{API_BASE}/api/send-image", 
                files={'file': f},
                data={'phone': TEST_PHONE, 'caption': '📸 Test image'}
            )
        print(f"Image: {response.status_code} - {response.json()}")
    except FileNotFoundError:
        print("Image: Skipped (no test.jpg file)")
    
    # Test document (if you have test.pdf)
    try:
        with open('test.pdf', 'rb') as f:
            response = requests.post(f"{API_BASE}/api/send-document",
                files={'file': f}, 
                data={'phone': TEST_PHONE, 'caption': '📄 Test document'}
            )
        print(f"Document: {response.status_code} - {response.json()}")
    except FileNotFoundError:
        print("Document: Skipped (no test.pdf file)")

if __name__ == "__main__":
    test_all_endpoints()
```

---

## ⚡ Rate Limits

**Current Status:** No rate limiting implemented

**Recommendations for Production:**
- Implement rate limiting per IP/user
- Suggested limits: 100 requests per hour
- Use Redis or in-memory storage for rate limiting
- Return 429 status code when exceeded

**Example Implementation:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/send-message', methods=['POST'])
@limiter.limit("10 per minute")
def send_message():
    # endpoint implementation
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Bot Not Connected
**Error:** `"Bot not connected"`

**Solution:**
- Check if WhatsApp bot is connected
- Restart the application
- Scan QR code with WhatsApp
- Check API status endpoint

#### 2. Invalid Phone Number
**Error:** `"Invalid phone number format"`

**Solution:**
- Use proper phone number format
- Include country code for international numbers
- Remove special characters except +

#### 3. File Too Large
**Error:** `"File too large. Max size for images: 16MB"`

**Solution:**
- Compress the file
- Check file size limits per media type
- Use appropriate compression tools

#### 4. Unsupported File Type
**Error:** `"Invalid file type. Allowed: ['mp3', 'wav', 'ogg']"`

**Solution:**
- Convert file to supported format
- Check supported extensions for each media type
- Use online converters if needed

#### 5. Connection Timeout
**Error:** `"Message sending timeout"`

**Solution:**
- Check internet connection
- Try smaller file sizes
- Wait and retry
- Check server resources

### Debug Mode

To enable debug mode, set environment variable:
```bash
export FLASK_DEBUG=1
python3 app.py
```

### Health Check

Always check bot status before sending messages:
```bash
curl http://localhost:5000/api/status
```

Ensure `bot_connected: true` before sending messages.

---

## 🔒 Security Considerations

### Production Deployment

1. **Authentication:**
   - Add API key authentication
   - Implement JWT tokens
   - Use HTTPS in production

2. **Rate Limiting:**
   - Implement per-user limits
   - Use Redis for distributed limiting
   - Monitor abuse patterns

3. **File Validation:**
   - Scan files for malware
   - Validate file content, not just extension
   - Implement file quarantine

4. **Logging:**
   - Log all API requests
   - Monitor error patterns
   - Implement audit trails

### Example Security Headers
```python
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

---

## 📞 Support

For issues and questions:
- Check this documentation first
- Review error messages carefully
- Test with minimal examples
- Check bot connection status

**API Version:** 2.0.0  
**Last Updated:** August 15, 2025  
**Status:** Production Ready ✅
