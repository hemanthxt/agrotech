"""
Start Streamlit with ngrok tunnel for public mobile access
Run this to get a public URL that works from anywhere
"""
import subprocess
import time
import os
from pyngrok import ngrok

PORT = 8501

print("🚀 Starting Agricultural Assistant with ngrok...")
print("=" * 60)

# Start Streamlit in background
streamlit_cmd = [
    "C:/Users/heman/AppData/Local/Programs/Python/Python311/python.exe",
    "-m",
    "streamlit",
    "run",
    "app_enhanced.py",
    "--server.port",
    str(PORT),
    "--server.address",
    "localhost",
]

print("📱 Starting Streamlit server...")
process = subprocess.Popen(streamlit_cmd)

# Give Streamlit time to start
print("⏳ Waiting for server to start...")
time.sleep(5)

# Create ngrok tunnel
print("🌐 Creating public tunnel...")
public_url = ngrok.connect(PORT, "http")

print("\n" + "=" * 60)
print("✅ SUCCESS! Your app is now accessible from mobile!")
print("=" * 60)
print(f"\n📱 MOBILE URL: {public_url}")
print(f"\n💻 Local URL: http://localhost:{PORT}")
print("\n" + "=" * 60)
print("\n📝 Instructions:")
print("1. Copy the Mobile URL above")
print("2. Open it in your mobile browser")
print("3. The app works from anywhere (not just WiFi)!")
print("\n⚠️  Keep this window open while using the app")
print("⚠️  Press Ctrl+C to stop\n")

try:
    # Keep running
    process.wait()
except KeyboardInterrupt:
    print("\n\n🛑 Stopping services...")
    ngrok.disconnect(public_url)
    ngrok.kill()
    process.terminate()
    print("✅ Stopped successfully!")
