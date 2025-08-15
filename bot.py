import asyncio
import threading
import logging
import os
import mimetypes
from neonize.aioze.client import NewAClient
from neonize.events import ConnectedEv, MessageEv, PairStatusEv
import time

class WhatsAppBot:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.client = NewAClient("data/db.sqlite3")
        self.is_connected = False
        self.loop = None
        self.thread = None
        self.logger = logging.getLogger(__name__)
        print("📁 Database: data/db.sqlite3")
        
    def start(self):
        """Start bot in background thread"""
        self.thread = threading.Thread(target=self._run_bot)
        self.thread.daemon = True
        self.thread.start()
        print("🔄 Bot thread started...")
        
    def _run_bot(self):
        """Run bot with asyncio"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        @self.client.event(ConnectedEv)
        async def on_connected(client, event):
            self.is_connected = True
            print("✅ WhatsApp Bot Connected Successfully!")
            print("🤖 Bot siap menerima dan mengirim pesan!")
            
        @self.client.event(PairStatusEv)
        async def on_pair_status(client, event):
            print(f"📱 Login sebagai: {event.ID.User}")
            
        @self.client.event(MessageEv)
        async def on_message(client, message):
            try:
                if message.Info.MessageSource.IsFromMe:
                    return
                    
                chat = message.Info.MessageSource.Chat
                text = ""
                if hasattr(message.Message, 'conversation') and message.Message.conversation:
                    text = message.Message.conversation
                elif hasattr(message.Message, 'extendedTextMessage') and message.Message.extendedTextMessage:
                    if hasattr(message.Message.extendedTextMessage, 'text'):
                        text = message.Message.extendedTextMessage.text
                
                if text:
                    print(f"📨 Pesan masuk dari {chat}: {text}")
                    
            except Exception as e:
                print(f"❌ Error handling message: {e}")
                
        try:
            print("🔄 Connecting to WhatsApp...")
            print("📱 QR Code akan muncul - scan dengan WhatsApp")
            print("-" * 50)
            
            self.loop.run_until_complete(self.client.connect())
            
        except Exception as e:
            print(f"❌ Bot connection error: {e}")
            
    def create_jid(self, phone_number):
        """Create proper JID object with all required fields"""
        try:
            from neonize.utils.jid import JID
            
            # Format phone number
            if "@" not in phone_number:
                clean_phone = ''.join(filter(str.isdigit, phone_number))
                if clean_phone.startswith('0'):
                    clean_phone = '62' + clean_phone[1:]
                elif not clean_phone.startswith('62'):
                    clean_phone = '62' + clean_phone
                phone_number = f"{clean_phone}@s.whatsapp.net"
            
            # Parse JID string
            parts = phone_number.split('@')
            if len(parts) != 2:
                raise ValueError(f"Invalid JID format: {phone_number}")
                
            user_part = parts[0]
            server_part = parts[1]
            
            # Create JID with all required fields
            jid = JID()
            jid.User = user_part
            jid.Server = server_part
            jid.RawAgent = 0
            jid.Device = 0
            jid.Integrator = 0
            jid.IsEmpty = False
            
            return jid
                
        except Exception as e:
            print(f"❌ Error creating JID: {e}")
            return None
            
    async def send_message_async(self, phone, message):
        """Send text message using the working method"""
        try:
            if not self.is_connected:
                return {"status": "error", "message": "Bot not connected to WhatsApp"}
            
            print(f"📤 Sending text to: {phone}")
            print(f"💬 Message: {message}")
            
            jid = self.create_jid(phone)
            if not jid:
                return {"status": "error", "message": "Failed to create JID object"}
            
            try:
                print("🔄 Trying build_reply_message...")
                
                built_message = await self.client.build_reply_message(
                    message=str(message),
                    quoted=None
                )
                
                if built_message and hasattr(built_message, 'SerializeToString'):
                    print(f"📦 Built message: {type(built_message)}")
                    
                    result = await self.client.send_message(jid, built_message)
                    print(f"✅ Text message sent successfully!")
                    
                    return {
                        "status": "success", 
                        "message": "Message sent successfully",
                        "data": {
                            "jid": f"{jid.User}@{jid.Server}", 
                            "text": message,
                            "method": "build_reply_message",
                            "timestamp": time.time()
                        }
                    }
                else:
                    print("⚠️ build_reply_message returned None")
                    raise Exception("build_reply_message returned None")
                    
            except Exception as e1:
                print(f"⚠️ build_reply_message failed: {e1}")
                
                try:
                    print("🔄 Trying direct message creation...")
                    
                    from neonize.proto.waE2E.WAWebProtobufsE2E_pb2 import Message
                    
                    msg = Message()
                    msg.conversation = str(message)
                    
                    result = await self.client.send_message(jid, msg)
                    print(f"✅ Message sent using direct creation!")
                    
                    return {
                        "status": "success",
                        "message": "Message sent successfully", 
                        "data": {
                            "jid": f"{jid.User}@{jid.Server}",
                            "text": message,
                            "method": "direct_message",
                            "timestamp": time.time()
                        }
                    }
                    
                except Exception as e2:
                    print(f"❌ All text methods failed: {e1} | {e2}")
                    return {"status": "error", "message": f"Failed to send text: {e2}"}
            
        except Exception as e:
            print(f"❌ General error sending text: {e}")
            return {"status": "error", "message": str(e)}
    
    async def send_image_async(self, phone, filepath, caption=""):
        """Send image with optional caption"""
        try:
            if not self.is_connected:
                return {"status": "error", "message": "Bot not connected to WhatsApp"}
            
            print(f"📤 Sending image to: {phone}")
            print(f"🖼️ File: {filepath}")
            print(f"📝 Caption: {caption}")
            
            jid = self.create_jid(phone)
            if not jid:
                return {"status": "error", "message": "Failed to create JID object"}
            
            if not os.path.exists(filepath):
                return {"status": "error", "message": "File not found"}
            
            try:
                built_message = await self.client.build_image_message(
                    file=filepath,
                    caption=caption if caption else None,
                    quoted=None
                )
                
                if built_message:
                    result = await self.client.send_message(jid, built_message)
                    print(f"✅ Image sent successfully!")
                    
                    return {
                        "status": "success",
                        "message": "Image sent successfully",
                        "data": {
                            "jid": f"{jid.User}@{jid.Server}",
                            "filepath": filepath,
                            "caption": caption,
                            "timestamp": time.time()
                        }
                    }
                else:
                    return {"status": "error", "message": "Failed to build image message"}
                    
            except Exception as e:
                print(f"❌ Error sending image: {e}")
                return {"status": "error", "message": str(e)}
            
        except Exception as e:
            print(f"❌ General error sending image: {e}")
            return {"status": "error", "message": str(e)}
    
    async def send_document_async(self, phone, filepath, caption="", filename=None):
        """Send document with optional caption"""
        try:
            if not self.is_connected:
                return {"status": "error", "message": "Bot not connected to WhatsApp"}
            
            print(f"📤 Sending document to: {phone}")
            print(f"📄 File: {filepath}")
            print(f"📝 Caption: {caption}")
            print(f"📋 Filename: {filename}")
            
            jid = self.create_jid(phone)
            if not jid:
                return {"status": "error", "message": "Failed to create JID object"}
            
            if not os.path.exists(filepath):
                return {"status": "error", "message": "File not found"}
            
            try:
                # Get mimetype
                mimetype, _ = mimetypes.guess_type(filepath)
                if not mimetype:
                    mimetype = 'application/octet-stream'
                
                # Use provided filename or extract from path
                if not filename:
                    filename = os.path.basename(filepath)
                
                print(f"📋 Mimetype: {mimetype}")
                
                built_message = await self.client.build_document_message(
                    file=filepath,
                    caption=caption if caption else None,
                    title=filename,
                    filename=filename,
                    mimetype=mimetype,
                    quoted=None
                )
                
                if built_message:
                    result = await self.client.send_message(jid, built_message)
                    print(f"✅ Document sent successfully!")
                    
                    return {
                        "status": "success",
                        "message": "Document sent successfully",
                        "data": {
                            "jid": f"{jid.User}@{jid.Server}",
                            "filepath": filepath,
                            "filename": filename,
                            "caption": caption,
                            "mimetype": mimetype,
                            "timestamp": time.time()
                        }
                    }
                else:
                    return {"status": "error", "message": "Failed to build document message"}
                    
            except Exception as e:
                print(f"❌ Error sending document: {e}")
                return {"status": "error", "message": str(e)}
            
        except Exception as e:
            print(f"❌ General error sending document: {e}")
            return {"status": "error", "message": str(e)}
    
    async def send_audio_async(self, phone, filepath):
        """Send audio file"""
        try:
            if not self.is_connected:
                return {"status": "error", "message": "Bot not connected to WhatsApp"}
            
            print(f"📤 Sending audio to: {phone}")
            print(f"🎵 File: {filepath}")
            
            jid = self.create_jid(phone)
            if not jid:
                return {"status": "error", "message": "Failed to create JID object"}
            
            if not os.path.exists(filepath):
                return {"status": "error", "message": "File not found"}
            
            try:
                built_message = await self.client.build_audio_message(
                    file=filepath,
                    quoted=None
                )
                
                if built_message:
                    result = await self.client.send_message(jid, built_message)
                    print(f"✅ Audio sent successfully!")
                    
                    return {
                        "status": "success",
                        "message": "Audio sent successfully",
                        "data": {
                            "jid": f"{jid.User}@{jid.Server}",
                            "filepath": filepath,
                            "timestamp": time.time()
                        }
                    }
                else:
                    return {"status": "error", "message": "Failed to build audio message"}
                    
            except Exception as e:
                print(f"❌ Error sending audio: {e}")
                return {"status": "error", "message": str(e)}
            
        except Exception as e:
            print(f"❌ General error sending audio: {e}")
            return {"status": "error", "message": str(e)}
    
    async def send_video_async(self, phone, filepath, caption=""):
        """Send video with optional caption"""
        try:
            if not self.is_connected:
                return {"status": "error", "message": "Bot not connected to WhatsApp"}
            
            print(f"📤 Sending video to: {phone}")
            print(f"🎬 File: {filepath}")
            print(f"📝 Caption: {caption}")
            
            jid = self.create_jid(phone)
            if not jid:
                return {"status": "error", "message": "Failed to create JID object"}
            
            if not os.path.exists(filepath):
                return {"status": "error", "message": "File not found"}
            
            try:
                built_message = await self.client.build_video_message(
                    file=filepath,
                    caption=caption if caption else None,
                    quoted=None
                )
                
                if built_message:
                    result = await self.client.send_message(jid, built_message)
                    print(f"✅ Video sent successfully!")
                    
                    return {
                        "status": "success",
                        "message": "Video sent successfully",
                        "data": {
                            "jid": f"{jid.User}@{jid.Server}",
                            "filepath": filepath,
                            "caption": caption,
                            "timestamp": time.time()
                        }
                    }
                else:
                    return {"status": "error", "message": "Failed to build video message"}
                    
            except Exception as e:
                print(f"❌ Error sending video: {e}")
                return {"status": "error", "message": str(e)}
            
        except Exception as e:
            print(f"❌ General error sending video: {e}")
            return {"status": "error", "message": str(e)}
    
    async def send_sticker_async(self, phone, filepath):
        """Send sticker (WebP format)"""
        try:
            if not self.is_connected:
                return {"status": "error", "message": "Bot not connected to WhatsApp"}
            
            print(f"📤 Sending sticker to: {phone}")
            print(f"🎨 File: {filepath}")
            
            jid = self.create_jid(phone)
            if not jid:
                return {"status": "error", "message": "Failed to create JID object"}
            
            if not os.path.exists(filepath):
                return {"status": "error", "message": "File not found"}
            
            try:
                built_message = await self.client.build_sticker_message(
                    file=filepath,
                    quoted=None
                )
                
                if built_message:
                    result = await self.client.send_message(jid, built_message)
                    print(f"✅ Sticker sent successfully!")
                    
                    return {
                        "status": "success",
                        "message": "Sticker sent successfully",
                        "data": {
                            "jid": f"{jid.User}@{jid.Server}",
                            "filepath": filepath,
                            "timestamp": time.time()
                        }
                    }
                else:
                    return {"status": "error", "message": "Failed to build sticker message"}
                    
            except Exception as e:
                print(f"❌ Error sending sticker: {e}")
                return {"status": "error", "message": str(e)}
            
        except Exception as e:
            print(f"❌ General error sending sticker: {e}")
            return {"status": "error", "message": str(e)}
    
    # Thread-safe wrapper methods
    def send_message(self, phone, message):
        """Thread-safe text message sending"""
        if not self.loop:
            return {"status": "error", "message": "Bot not started"}
            
        if not self.is_connected:
            return {"status": "error", "message": "Bot not connected. Please scan QR code first."}
        
        try:
            future = asyncio.run_coroutine_threadsafe(
                self.send_message_async(phone, message), 
                self.loop
            )
            return future.result(timeout=30)
        except asyncio.TimeoutError:
            return {"status": "error", "message": "Message sending timeout"}
        except Exception as e:
            return {"status": "error", "message": f"Wrapper error: {str(e)}"}
    
    def send_image(self, phone, filepath, caption=""):
        """Thread-safe image sending"""
        if not self.loop:
            return {"status": "error", "message": "Bot not started"}
            
        if not self.is_connected:
            return {"status": "error", "message": "Bot not connected. Please scan QR code first."}
        
        try:
            future = asyncio.run_coroutine_threadsafe(
                self.send_image_async(phone, filepath, caption), 
                self.loop
            )
            return future.result(timeout=60)
        except asyncio.TimeoutError:
            return {"status": "error", "message": "Image sending timeout"}
        except Exception as e:
            return {"status": "error", "message": f"Wrapper error: {str(e)}"}
    
    def send_document(self, phone, filepath, caption="", filename=None):
        """Thread-safe document sending"""
        if not self.loop:
            return {"status": "error", "message": "Bot not started"}
            
        if not self.is_connected:
            return {"status": "error", "message": "Bot not connected. Please scan QR code first."}
        
        try:
            future = asyncio.run_coroutine_threadsafe(
                self.send_document_async(phone, filepath, caption, filename), 
                self.loop
            )
            return future.result(timeout=60)
        except asyncio.TimeoutError:
            return {"status": "error", "message": "Document sending timeout"}
        except Exception as e:
            return {"status": "error", "message": f"Wrapper error: {str(e)}"}
    
    def send_audio(self, phone, filepath):
        """Thread-safe audio sending"""
        if not self.loop:
            return {"status": "error", "message": "Bot not started"}
            
        if not self.is_connected:
            return {"status": "error", "message": "Bot not connected. Please scan QR code first."}
        
        try:
            future = asyncio.run_coroutine_threadsafe(
                self.send_audio_async(phone, filepath), 
                self.loop
            )
            return future.result(timeout=90)  # Longer timeout for audio
        except asyncio.TimeoutError:
            return {"status": "error", "message": "Audio sending timeout"}
        except Exception as e:
            return {"status": "error", "message": f"Wrapper error: {str(e)}"}
    
    def send_video(self, phone, filepath, caption=""):
        """Thread-safe video sending"""
        if not self.loop:
            return {"status": "error", "message": "Bot not started"}
            
        if not self.is_connected:
            return {"status": "error", "message": "Bot not connected. Please scan QR code first."}
        
        try:
            future = asyncio.run_coroutine_threadsafe(
                self.send_video_async(phone, filepath, caption), 
                self.loop
            )
            return future.result(timeout=120)  # Longer timeout for video
        except asyncio.TimeoutError:
            return {"status": "error", "message": "Video sending timeout"}
        except Exception as e:
            return {"status": "error", "message": f"Wrapper error: {str(e)}"}
    
    def send_sticker(self, phone, filepath):
        """Thread-safe sticker sending"""
        if not self.loop:
            return {"status": "error", "message": "Bot not started"}
            
        if not self.is_connected:
            return {"status": "error", "message": "Bot not connected. Please scan QR code first."}
        
        try:
            future = asyncio.run_coroutine_threadsafe(
                self.send_sticker_async(phone, filepath), 
                self.loop
            )
            return future.result(timeout=30)
        except asyncio.TimeoutError:
            return {"status": "error", "message": "Sticker sending timeout"}
        except Exception as e:
            return {"status": "error", "message": f"Wrapper error: {str(e)}"}
            
    def is_alive(self):
        """Check if bot thread is alive"""
        return self.thread and self.thread.is_alive()
        
    def stop(self):
        """Stop the bot"""
        if self.loop and not self.loop.is_closed():
            self.loop.call_soon_threadsafe(self.loop.stop)
        if self.thread:
            self.thread.join(timeout=5)
        self.is_connected = False
        print("🛑 Bot stopped")

# Global bot instance
bot_instance = WhatsAppBot()
