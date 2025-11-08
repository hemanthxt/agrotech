import subprocess
import time
import os
from pyngrok import ngrok

# Optional: set your ngrok authtoken here or run `pyngrok authtoken <TOKEN>` once beforehand
NGROK_AUTH_TOKEN = os.environ.get("NGROK_AUTHTOKEN", None)
PORT = 8501

if NGROK_AUTH_TOKEN:
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# Start streamlit bound to localhost:8501 but listening on 0.0.0.0 so ngrok can forward
streamlit_cmd = [
    "C:/Users/heman/AppData/Local/Programs/Python/Python311/python.exe",
    "-m",
    "streamlit",
    "run",
    "app.py",
    "--server.port",
    str(PORT),
    "--server.address",
    "0.0.0.0",
]

print("Starting Streamlit...")
process = subprocess.Popen(streamlit_cmd)

# Give Streamlit some time to start
time.sleep(3)

print("Opening ngrok tunnel...")
public_url = ngrok.connect(PORT, "http").public_url
print(f"ngrok public URL: {public_url}")
print("Press Ctrl+C to stop both Streamlit and ngrok.")

try:
    process.wait()
except KeyboardInterrupt:
    print("Stopping Streamlit and ngrok...")
    ngrok.disconnect(public_url)
    ngrok.kill()
    process.terminate()
