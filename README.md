# 🌾 Agri Assistant - Native Mobile App

**Agricultural Assistant for Farmers** - Weather monitoring, price tracking, financial planning, and irrigation management.

## 📱 Download Android APK

**[📥 Download Latest APK](../../releases/latest)** ← Click here to get the mobile app!

The APK is automatically built when code is pushed to GitHub. Install it on your Android phone and use offline!

---

## Features

✅ **Weather Monitoring** - Real-time weather data with forecasts  
✅ **Price Tracking** - Current market prices for 170+ crops  
✅ **Financial Calculator** - Cost estimation and profit analysis  
✅ **Irrigation Calculator** - Water requirement calculations  
✅ **Farm Calendar** - Crop scheduling and growth stages  
✅ **Crop Rotation Planner** - Multi-year rotation optimization  
✅ **Fertilizer Calculator** - NPK recommendations  
✅ **170+ Crops Support** - Grains, fruits, vegetables, flowers, herbs, cash crops  
✅ **Offline Support** - Works without internet after initial data download  
✅ **GPS Location** - Auto-detect your farm location  

---

## 🚀 Quick Start

### Option 1: Mobile App (APK)
1. Download APK from [Releases](../../releases/latest)
2. Install on Android phone
3. Open and use offline!

### Option 2: Web Version
This project also has a Streamlit web app that runs locally.

## Requirements
- Python 3.11
- The project dependencies (install with pip)

Install dependencies:

```powershell
C:/Users/heman/AppData/Local/Programs/Python/Python311/python.exe -m pip install -r requirements.txt
```

If you don't have a `requirements.txt`, you can install the core libs:

```powershell
C:/Users/heman/AppData/Local/Programs/Python/Python311/python.exe -m pip install streamlit pandas plotly requests numpy pyngrok
```

## Run locally and access from mobile on the same Wi-Fi
1. Find your PC's local IP address (PowerShell):

```powershell
ipconfig | Select-String "IPv4" -Context 0,0
```

2. Start Streamlit so it listens on all interfaces (0.0.0.0) and a fixed port (e.g., 8501):

```powershell
C:/Users/heman/AppData/Local/Programs/Python/Python311/python.exe -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

3. On your mobile device connected to the same Wi-Fi, open a browser and go to:

```
http://<PC_LOCAL_IP>:8501
```

Replace `<PC_LOCAL_IP>` with the address found in step 1.

Notes:
- Windows Firewall may block incoming connections. If the mobile device can't connect, temporarily allow the port or create a firewall rule for the Python executable or port 8501.
- Some routers have client isolation on guest networks which prevents devices from talking to each other. Ensure both devices are on the same local network and not isolated.

## Get a public URL using ngrok (optional)
1. Install `pyngrok`:

```powershell
C:/Users/heman/AppData/Local/Programs/Python/Python311/python.exe -m pip install pyngrok
```

2. Create an ngrok authtoken at https://dashboard.ngrok.com/get-started/your-authtoken and run:

```powershell
pyngrok authtoken <YOUR_TOKEN>
```

3. Run the helper script which will start Streamlit and open an ngrok tunnel:

```powershell
C:/Users/heman/AppData/Local/Programs/Python/Python311/python.exe run_ngrok.py
```

The script prints a public HTTPS URL you can open from mobile anywhere.

Security note: Exposing your app to the public internet can be risky. Only expose services you trust and consider adding authentication.

## Provided helper scripts
- `run_local.ps1` — PowerShell script to run Streamlit bound to 0.0.0.0 on port 8501
- `run_ngrok.py` — Python helper that starts Streamlit as a subprocess and creates an ngrok tunnel. Modify `NGROK_AUTH_TOKEN` or run `pyngrok authtoken <token>` once.

---
If you'd like, I can start an ngrok tunnel now and return the public URL (requires your approval).