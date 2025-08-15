# 🚀 WhatsApp API Complete

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![Neonize](https://img.shields.io/badge/Neonize-0.3.11-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

**Complete WhatsApp REST API with comprehensive media support**

*Send text, images, documents, audio, video & stickers programmatically*

</div>

---

## ✨ Features

### 📱 **Complete Media Support**
- ✅ **Text Messages** - Rich text with emojis
- ✅ **Images** - JPG, PNG, GIF, WebP with captions
- ✅ **Documents** - PDF, Office files, archives
- ✅ **Audio** - MP3, WAV, OGG, M4A, AAC, FLAC
- ✅ **Video** - MP4, AVI, MOV, MKV with captions
- ✅ **Stickers** - WebP format stickers

### 🔧 **Production Features**
- ✅ **REST API** - Clean JSON endpoints
- ✅ **File Validation** - Type & size checking
- ✅ **Error Handling** - Comprehensive error responses
- ✅ **Auto Cleanup** - Temporary files management
- ✅ **Phone Formatting** - International number support
- ✅ **Concurrent Requests** - Thread-safe operations

### 🎯 **Developer Friendly**
- ✅ **Easy Setup** - One-command installation
- ✅ **Detailed Docs** - Complete API documentation
- ✅ **Code Examples** - Multiple programming languages
- ✅ **Error Messages** - Clear troubleshooting info

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- WhatsApp account for QR scanning
- Linux/Ubuntu server (recommended)

### Installation

```bash
# Clone repository
git clone https://github.com/classyid/neonize-whatsapp-api.git
cd neonize-whatsapp-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p data logs uploads

# Start the API server
python3 app.py
```

### First Setup

1. **Start the server** - Run `python3 app.py`
2. **Scan QR Code** - Use WhatsApp app to scan the QR code that appears
3. **Test connection** - Check `http://localhost:5000/api/status`
4. **Send first message** - Use the examples below

---

## 📖 Documentation

### API Endpoints

| Endpoint | Method | Description | Media Support |
|----------|--------|-------------|---------------|
| `GET /` | GET | API health & info | - |
| `GET /api/status` | GET | Bot connection status | - |
| `POST /api/send-message` | POST | Send text message | Text |
| `POST /api/send-image` | POST | Send image with caption | Images |
| `POST /api/send-document` | POST | Send document with caption | Documents |
| `POST /api/send-audio` | POST | Send audio file | Audio |
| `POST /api/send-video` | POST | Send video with caption | Video |
| `POST /api/send-sticker` | POST | Send WebP sticker | Stickers |

### Supported File Types

| Media Type | Extensions | Max Size | Caption |
|------------|------------|----------|---------|
| **Images** | jpg, jpeg, png, gif, webp | 16MB | ✅ |
| **Documents** | pdf, doc, docx, xls, xlsx, ppt, pptx, txt, zip, rar, 7z | 32MB | ✅ |
| **Audio** | mp3, wav, ogg, m4a, aac, flac | 16MB | ❌ |
| **Video** | mp4, avi, mov, mkv, webm, 3gp, flv | 64MB | ✅ |
| **Stickers** | webp | 1MB | ❌ |

---

## 🧪 Examples

### Send Text Message

```bash
curl -X POST http://localhost:5000/api/send-message \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "6281234567890",
    "message": "Hello from WhatsApp API! 🚀"
  }'
```

### Send Image with Caption

```bash
curl -X POST http://localhost:5000/api/send-image \
  -F "phone=6281234567890" \
  -F "caption=📸 Beautiful sunset!" \
  -F "file=@image.jpg"
```

### Send Document

```bash
curl -X POST http://localhost:5000/api/send-document \
  -F "phone=6281234567890" \
  -F "caption=📄 Important report" \
  -F "file=@report.pdf"
```

### Send Audio

```bash
curl -X POST http://localhost:5000/api/send-audio \
  -F "phone=6281234567890" \
  -F "file=@voice_message.mp3"
```

### Send Video

```bash
curl -X POST http://localhost:5000/api/send-video \
  -F "phone=6281234567890" \
  -F "caption=🎬 Demo video" \
  -F "file=@demo.mp4"
```

### Python Example

```python
import requests

# Send text message
response = requests.post('http://localhost:5000/api/send-message', json={
    "phone": "6281234567890",
    "message": "Hello from Python! 🐍"
})

print(response.json())

# Send image
with open('image.jpg', 'rb') as f:
    response = requests.post('http://localhost:5000/api/send-image', 
        files={'file': f},
        data={'phone': '6281234567890', 'caption': '📸 Python image'}
    )
    
print(response.json())
```

### JavaScript Example

```javascript
// Send text message
const response = await fetch('http://localhost:5000/api/send-message', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    phone: '6281234567890',
    message: 'Hello from JavaScript! 🌟'
  })
});

const result = await response.json();
console.log(result);

// Send image
const formData = new FormData();
formData.append('phone', '6281234567890');
formData.append('caption', '📸 JavaScript image');
formData.append('file', fileInput.files[0]);

const imageResponse = await fetch('http://localhost:5000/api/send-image', {
  method: 'POST',
  body: formData
});

console.log(await imageResponse.json());
```

---

## 🌐 Response Format

### Success Response
```json
{
  "status": "success",
  "message": "Message sent successfully",
  "data": {
    "phone": "6281234567890",
    "message": "Hello World!",
    "type": "text",
    "timestamp": "2025-08-15 17:38:34.475734"
  }
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Bot not connected"
}
```

---

## 🚀 Deployment

### Development Server
```bash
python3 app.py
# Runs on http://localhost:5000
```

### Production with Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run production server
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN mkdir -p data logs uploads

EXPOSE 5000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
```

```bash
# Build and run
docker build -t whatsapp-api .
docker run -p 5000:5000 -v $(pwd)/data:/app/data whatsapp-api
```

### Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 🔧 Configuration

### Environment Variables
```bash
# .env file
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

BOT_NAME=WhatsApp_API_Bot
DATABASE_PATH=./data/db.sqlite3
UPLOAD_FOLDER=./uploads
MAX_FILE_SIZE=67108864  # 64MB

LOG_LEVEL=INFO
LOG_DIR=./logs
```

### File Size Limits
- **Images**: 16MB
- **Documents**: 32MB  
- **Audio**: 16MB
- **Video**: 64MB
- **Stickers**: 1MB

### Phone Number Format
The API accepts various phone number formats:
- `081234567890` (Indonesian local)
- `+6281234567890` (International)
- `6281234567890` (Without +)

All formats are automatically converted to WhatsApp format.

---

## 🔍 Troubleshooting

### Bot Not Connected
```bash
# Check bot status
curl http://localhost:5000/api/status

# Restart if needed
Ctrl+C
python3 app.py
# Scan QR code again
```

### File Upload Issues
- Check file size limits
- Verify file extension is supported
- Ensure stable internet connection

### Common Errors
- `"Invalid phone number"` - Use proper format with country code
- `"File too large"` - Compress file or check size limits
- `"Invalid file type"` - Convert to supported format

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/classyid/neonize-whatsapp-api.git

# Install development dependencies
pip install -r requirements.txt
pip install black flake8 pytest

# Run tests
python -m pytest tests/

# Format code
black app.py bot.py
```

---

## 📊 Technical Stack

- **Backend**: Python 3.10+ with Flask 2.3+
- **WhatsApp**: Neonize 0.3.11 library
- **Database**: SQLite (session storage)
- **File Upload**: Werkzeug secure handling
- **Async**: Threading for concurrent operations

---

## ⚠️ Disclaimer

This project is for educational and development purposes. Please ensure compliance with:
- WhatsApp Terms of Service
- Local regulations regarding automated messaging
- Data privacy laws (GDPR, etc.)

**Use responsibly and respect recipients' privacy.**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Neonize** - WhatsApp Web API library
- **Flask** - Web framework
- **WhatsApp** - Messaging platform
- **Community** - Contributors and users

---

<div align="center">

**⭐ Star this repository if it helped you!**

Made with ❤️ for developers who build amazing things

[🚀 Get Started](#-quick-start) 

</div>
