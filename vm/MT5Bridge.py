import MetaTrader5 as mt5
import json, os

# === Paths ===
BASE_DIR = os.path.dirname(__file__)
LOGIN_FILE = os.path.join(BASE_DIR, "login.json")
WATCHLIST_FILE = os.path.join(BASE_DIR, "watchlist.json")

# === Load credentials ===
def load_creds():
    try:
        with open(LOGIN_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# === Load watchlist ===
def load_watchlist():
    try:
        with open(WATCHLIST_FILE, "r") as f:
            return json.load(f)
    except:
        return ["EURUSD", "GBPUSD", "XAUUSD"]  # fallback

# === Constants ===
MT5_PATH = os.getenv("MT5_PATH", "C:\\Users\\PROF\\Desktop\\SentinelBot_FullProject\\vm\\terminal64.exe")

# === MT5 Connect (dynamic or static) ===
def connect_mt5(login=None, server=None, password=None):
    if login and server and password:
        if not mt5.initialize(MT5_PATH, login=login, server=server, password=password):
            raise RuntimeError(f"❌ MT5 init failed: {mt5.last_error()}")
        return True
    else:
        creds = load_creds()
        if not mt5.initialize(MT5_PATH, login=int(creds["login"]), server=creds["server"], password=creds["password"]):
            raise RuntimeError(f"❌ MT5 login failed: {mt5.last_error()}")
        print("✅ MT5 login successful.")
        return True

# === Place Order (multi-user) ===
def place_order(symbol, direction, lot, sl, tp, login, server, password):
    connect_mt5(login, server, password)
    tick = mt5.symbol_info_tick(symbol)
    price = tick.ask if direction == "buy" else tick.bid
    order_type = mt5.ORDER_TYPE_BUY if direction == "buy" else mt5.ORDER_TYPE_SELL

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 20,
        "magic": 123456,
        "comment": "SentinelBot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    return result

# === Auto-activate symbols from watchlist ===
def activate_symbols(symbols):
    for symbol in symbols:
        mt5.symbol_select(symbol, True)
        print(f"📡 Activated symbol: {symbol}")

# === Admin Run (watchlist init only) ===
if __name__ == "__main__":
    connect_mt5()  # static admin login
    activate_symbols(load_watchlist())
