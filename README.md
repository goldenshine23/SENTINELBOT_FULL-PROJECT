# Sentinel Neural-V™ Bot Backend

A multi-user automated trading bot API connected to MetaTrader 5 via a local VM bridge.

## 📁 Folder Structure

- `backend/` → FastAPI API (auth, payments, trade, admin)
- `vm/` → MT5 setup, login, and local bridge
- `.env` → MT5 path
- `requirements.txt` → Python dependencies

## 🛠️ Setup Instructions

1. Clone repo or extract folder  
2. Install Python 3.11+ and MetaTrader5  
3. Create venv and install requirements:

```bash
cd SentinelBot_FullProject
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
#   S E N T I N E L B O T _ F U L L - P R O J E C T  
 