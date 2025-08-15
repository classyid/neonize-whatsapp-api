from flask import Flask, request, jsonify
import re
import os
from werkzeug.utils import secure_filename
from bot import bot_instance
from datetime import datetime

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 64 * 1024 * 1024  # 64MB for video files
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'zip', 'rar', '7z'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg', 'm4a', 'aac', 'flac'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm', '3gp', 'flv'}
ALLOWED_STICKER_EXTENSIONS = {'webp'}

# File size limits per type
FILE_SIZE_LIMITS = {
    'image': 16 * 1024 * 1024,      # 16MB
    'document': 32 * 1024 * 1024,   # 32MB  
    'audio': 16 * 1024 * 1024,      # 16MB
    'video': 64 * 1024 * 1024,      # 64MB
    'sticker': 1 * 1024 * 1024      # 1MB
}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def validate_phone(phone):
    """Validate phone number format"""
    phone = re.sub(r'\D', '', phone)
    if len(phone) < 10 or len(phone) > 15:
        return None
    if phone.startswith('0'):
        phone = '62' + phone[1:]
    elif not phone.startswith('62'):
        phone = '62' + phone
    return phone

def get_file_type(filename):
    """Determine file type based on extension"""
    if '.' not in filename:
        return None
    extension = filename.rsplit('.', 1)[1].lower()
    
    if extension in ALLOWED_IMAGE_EXTENSIONS:
        return 'image'
    elif extension in ALLOWED_DOCUMENT_EXTENSIONS:
        return 'document'
    elif extension in ALLOWED_AUDIO_EXTENSIONS:
        return 'audio'
    elif extension in ALLOWED_VIDEO_EXTENSIONS:
        return 'video'
    elif extension in ALLOWED_STICKER_EXTENSIONS:
        return 'sticker'
    return None

def allowed_file(filename, expected_type):
    """Check if file is allowed type"""
    file_type = get_file_type(filename)
    return file_type == expected_type

def save_uploaded_file(file):
    """Save uploaded file and return path"""
    if file and file.filename:
        filename = secure_filename(file.filename)
        if filename:
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            return filepath
    return None

def validate_file_size(file_size, file_type):
    """Validate file size based on type"""
    max_size = FILE_SIZE_LIMITS.get(file_type, MAX_FILE_SIZE)
    return file_size <= max_size

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "service": "WhatsApp API - Complete Media Support",
        "status": "running",
        "bot_connected": bot_instance.is_connected,
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
            "images": list(ALLOWED_IMAGE_EXTENSIONS),
            "documents": list(ALLOWED_DOCUMENT_EXTENSIONS),
            "audio": list(ALLOWED_AUDIO_EXTENSIONS),
            "video": list(ALLOWED_VIDEO_EXTENSIONS),
            "stickers": list(ALLOWED_STICKER_EXTENSIONS)
        },
        "file_size_limits": {
            "images": f"{FILE_SIZE_LIMITS['image'] // (1024*1024)}MB",
            "documents": f"{FILE_SIZE_LIMITS['document'] // (1024*1024)}MB",
            "audio": f"{FILE_SIZE_LIMITS['audio'] // (1024*1024)}MB", 
            "video": f"{FILE_SIZE_LIMITS['video'] // (1024*1024)}MB",
            "stickers": f"{FILE_SIZE_LIMITS['sticker'] // (1024*1024)}MB"
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
    })

@app.route('/api/send-message', methods=['POST'])
def send_message():
    """Send text message (working perfectly)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"status": "error", "message": "JSON payload required"}), 400
            
        phone = data.get('phone')
        message = data.get('message')
        
        if not phone or not message:
            return jsonify({"status": "error", "message": "Phone and message required"}), 400
            
        formatted_phone = validate_phone(phone)
        if not formatted_phone:
            return jsonify({"status": "error", "message": "Invalid phone number"}), 400
            
        if not bot_instance.is_connected:
            return jsonify({"status": "error", "message": "Bot not connected"}), 503
            
        result = bot_instance.send_message(formatted_phone, message)
        
        if result["status"] == "success":
            return jsonify({
                "status": "success",
                "message": "Text message sent successfully",
                "data": {
                    "phone": formatted_phone,
                    "message": message,
                    "type": "text",
                    "timestamp": str(datetime.now())
                }
            }), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/send-image', methods=['POST'])
def send_image():
    """Send image with optional caption (working perfectly)"""
    try:
        if not bot_instance.is_connected:
            return jsonify({"status": "error", "message": "Bot not connected"}), 503
        
        phone = request.form.get('phone')
        if not phone:
            return jsonify({"status": "error", "message": "Phone number required"}), 400
            
        formatted_phone = validate_phone(phone)
        if not formatted_phone:
            return jsonify({"status": "error", "message": "Invalid phone number"}), 400
        
        caption = request.form.get('caption', '')
        
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "message": "No file selected"}), 400
        
        if not allowed_file(file.filename, 'image'):
            return jsonify({
                "status": "error", 
                "message": f"Invalid file type. Allowed: {list(ALLOWED_IMAGE_EXTENSIONS)}"
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if not validate_file_size(file_size, 'image'):
            return jsonify({
                "status": "error",
                "message": f"File too large. Max size for images: {FILE_SIZE_LIMITS['image'] // (1024*1024)}MB"
            }), 400
        
        filepath = save_uploaded_file(file)
        if not filepath:
            return jsonify({"status": "error", "message": "Failed to save file"}), 500
        
        try:
            result = bot_instance.send_image(formatted_phone, filepath, caption)
            
            try:
                os.remove(filepath)
            except:
                pass
            
            if result["status"] == "success":
                return jsonify({
                    "status": "success",
                    "message": "Image sent successfully",
                    "data": {
                        "phone": formatted_phone,
                        "filename": file.filename,
                        "caption": caption,
                        "type": "image",
                        "file_size_kb": round(file_size / 1024, 2),
                        "timestamp": str(datetime.now())
                    }
                }), 200
            else:
                return jsonify(result), 500
                
        except Exception as e:
            try:
                os.remove(filepath)
            except:
                pass
            raise e
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/send-document', methods=['POST'])
def send_document():
    """Send document with optional caption (working perfectly)"""
    try:
        if not bot_instance.is_connected:
            return jsonify({"status": "error", "message": "Bot not connected"}), 503
        
        phone = request.form.get('phone')
        if not phone:
            return jsonify({"status": "error", "message": "Phone number required"}), 400
            
        formatted_phone = validate_phone(phone)
        if not formatted_phone:
            return jsonify({"status": "error", "message": "Invalid phone number"}), 400
        
        caption = request.form.get('caption', '')
        
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "message": "No file selected"}), 400
        
        if not allowed_file(file.filename, 'document'):
            return jsonify({
                "status": "error", 
                "message": f"Invalid file type. Allowed: {list(ALLOWED_DOCUMENT_EXTENSIONS)}"
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if not validate_file_size(file_size, 'document'):
            return jsonify({
                "status": "error",
                "message": f"File too large. Max size for documents: {FILE_SIZE_LIMITS['document'] // (1024*1024)}MB"
            }), 400
        
        filepath = save_uploaded_file(file)
        if not filepath:
            return jsonify({"status": "error", "message": "Failed to save file"}), 500
        
        try:
            result = bot_instance.send_document(formatted_phone, filepath, caption, file.filename)
            
            try:
                os.remove(filepath)
            except:
                pass
            
            if result["status"] == "success":
                return jsonify({
                    "status": "success",
                    "message": "Document sent successfully",
                    "data": {
                        "phone": formatted_phone,
                        "filename": file.filename,
                        "caption": caption,
                        "type": "document",
                        "file_size_kb": round(file_size / 1024, 2),
                        "timestamp": str(datetime.now())
                    }
                }), 200
            else:
                return jsonify(result), 500
                
        except Exception as e:
            try:
                os.remove(filepath)
            except:
                pass
            raise e
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/send-audio', methods=['POST'])
def send_audio():
    """Send audio file"""
    try:
        if not bot_instance.is_connected:
            return jsonify({"status": "error", "message": "Bot not connected"}), 503
        
        phone = request.form.get('phone')
        if not phone:
            return jsonify({"status": "error", "message": "Phone number required"}), 400
            
        formatted_phone = validate_phone(phone)
        if not formatted_phone:
            return jsonify({"status": "error", "message": "Invalid phone number"}), 400
        
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "message": "No file selected"}), 400
        
        if not allowed_file(file.filename, 'audio'):
            return jsonify({
                "status": "error", 
                "message": f"Invalid file type. Allowed: {list(ALLOWED_AUDIO_EXTENSIONS)}"
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if not validate_file_size(file_size, 'audio'):
            return jsonify({
                "status": "error",
                "message": f"File too large. Max size for audio: {FILE_SIZE_LIMITS['audio'] // (1024*1024)}MB"
            }), 400
        
        filepath = save_uploaded_file(file)
        if not filepath:
            return jsonify({"status": "error", "message": "Failed to save file"}), 500
        
        try:
            result = bot_instance.send_audio(formatted_phone, filepath)
            
            try:
                os.remove(filepath)
            except:
                pass
            
            if result["status"] == "success":
                return jsonify({
                    "status": "success",
                    "message": "Audio sent successfully",
                    "data": {
                        "phone": formatted_phone,
                        "filename": file.filename,
                        "type": "audio",
                        "file_size_kb": round(file_size / 1024, 2),
                        "timestamp": str(datetime.now())
                    }
                }), 200
            else:
                return jsonify(result), 500
                
        except Exception as e:
            try:
                os.remove(filepath)
            except:
                pass
            raise e
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/send-video', methods=['POST'])
def send_video():
    """Send video with optional caption"""
    try:
        if not bot_instance.is_connected:
            return jsonify({"status": "error", "message": "Bot not connected"}), 503
        
        phone = request.form.get('phone')
        if not phone:
            return jsonify({"status": "error", "message": "Phone number required"}), 400
            
        formatted_phone = validate_phone(phone)
        if not formatted_phone:
            return jsonify({"status": "error", "message": "Invalid phone number"}), 400
        
        caption = request.form.get('caption', '')
        
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "message": "No file selected"}), 400
        
        if not allowed_file(file.filename, 'video'):
            return jsonify({
                "status": "error", 
                "message": f"Invalid file type. Allowed: {list(ALLOWED_VIDEO_EXTENSIONS)}"
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if not validate_file_size(file_size, 'video'):
            return jsonify({
                "status": "error",
                "message": f"File too large. Max size for video: {FILE_SIZE_LIMITS['video'] // (1024*1024)}MB"
            }), 400
        
        filepath = save_uploaded_file(file)
        if not filepath:
            return jsonify({"status": "error", "message": "Failed to save file"}), 500
        
        try:
            result = bot_instance.send_video(formatted_phone, filepath, caption)
            
            try:
                os.remove(filepath)
            except:
                pass
            
            if result["status"] == "success":
                return jsonify({
                    "status": "success",
                    "message": "Video sent successfully",
                    "data": {
                        "phone": formatted_phone,
                        "filename": file.filename,
                        "caption": caption,
                        "type": "video",
                        "file_size_kb": round(file_size / 1024, 2),
                        "timestamp": str(datetime.now())
                    }
                }), 200
            else:
                return jsonify(result), 500
                
        except Exception as e:
            try:
                os.remove(filepath)
            except:
                pass
            raise e
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/send-sticker', methods=['POST'])
def send_sticker():
    """Send WebP sticker"""
    try:
        if not bot_instance.is_connected:
            return jsonify({"status": "error", "message": "Bot not connected"}), 503
        
        phone = request.form.get('phone')
        if not phone:
            return jsonify({"status": "error", "message": "Phone number required"}), 400
            
        formatted_phone = validate_phone(phone)
        if not formatted_phone:
            return jsonify({"status": "error", "message": "Invalid phone number"}), 400
        
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "message": "No file selected"}), 400
        
        if not allowed_file(file.filename, 'sticker'):
            return jsonify({
                "status": "error", 
                "message": "Invalid file type. Stickers must be WebP format"
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if not validate_file_size(file_size, 'sticker'):
            return jsonify({
                "status": "error",
                "message": f"File too large. Max size for stickers: {FILE_SIZE_LIMITS['sticker'] // (1024*1024)}MB"
            }), 400
        
        filepath = save_uploaded_file(file)
        if not filepath:
            return jsonify({"status": "error", "message": "Failed to save file"}), 500
        
        try:
            result = bot_instance.send_sticker(formatted_phone, filepath)
            
            try:
                os.remove(filepath)
            except:
                pass
            
            if result["status"] == "success":
                return jsonify({
                    "status": "success",
                    "message": "Sticker sent successfully",
                    "data": {
                        "phone": formatted_phone,
                        "filename": file.filename,
                        "type": "sticker",
                        "file_size_kb": round(file_size / 1024, 2),
                        "timestamp": str(datetime.now())
                    }
                }), 200
            else:
                return jsonify(result), 500
                
        except Exception as e:
            try:
                os.remove(filepath)
            except:
                pass
            raise e
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/status', methods=['GET'])
def bot_status():
    return jsonify({
        "bot_connected": bot_instance.is_connected,
        "thread_alive": bot_instance.thread.is_alive() if bot_instance.thread else False,
        "upload_folder": UPLOAD_FOLDER,
        "supported_formats": {
            "images": list(ALLOWED_IMAGE_EXTENSIONS),
            "documents": list(ALLOWED_DOCUMENT_EXTENSIONS),
            "audio": list(ALLOWED_AUDIO_EXTENSIONS),
            "video": list(ALLOWED_VIDEO_EXTENSIONS),
            "stickers": list(ALLOWED_STICKER_EXTENSIONS)
        },
        "file_size_limits": {
            "images": f"{FILE_SIZE_LIMITS['image'] // (1024*1024)}MB",
            "documents": f"{FILE_SIZE_LIMITS['document'] // (1024*1024)}MB",
            "audio": f"{FILE_SIZE_LIMITS['audio'] // (1024*1024)}MB", 
            "video": f"{FILE_SIZE_LIMITS['video'] // (1024*1024)}MB",
            "stickers": f"{FILE_SIZE_LIMITS['sticker'] // (1024*1024)}MB"
        },
        "message": "Bot status retrieved"
    })

if __name__ == '__main__':
    print("🚀 Starting WhatsApp API Server...")
    print("📷 Image support: ✅ WORKING")
    print("📄 Document support: ✅ WORKING")
    print("🎵 Audio support: ✅ ENABLED")
    print("🎬 Video support: ✅ ENABLED")
    print("🎨 Sticker support: ✅ ENABLED")
    print(f"📂 Upload folder: {UPLOAD_FOLDER}")
    print(f"📏 File size limits:")
    print(f"   Images: {FILE_SIZE_LIMITS['image'] // (1024*1024)}MB")
    print(f"   Documents: {FILE_SIZE_LIMITS['document'] // (1024*1024)}MB")
    print(f"   Audio: {FILE_SIZE_LIMITS['audio'] // (1024*1024)}MB")
    print(f"   Video: {FILE_SIZE_LIMITS['video'] // (1024*1024)}MB")
    print(f"   Stickers: {FILE_SIZE_LIMITS['sticker'] // (1024*1024)}MB")
    print(f"🎵 Audio formats: {', '.join(ALLOWED_AUDIO_EXTENSIONS)}")
    print(f"🎬 Video formats: {', '.join(ALLOWED_VIDEO_EXTENSIONS)}")
    
    bot_instance.start()
    
    print("⏳ Waiting for WhatsApp connection...")
    print("📱 Scan QR code with WhatsApp")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
