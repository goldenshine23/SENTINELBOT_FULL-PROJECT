from datetime import datetime
import requests
import random

# === CONFIG ===

SYMBOLS = [
    "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD",
    "NZDUSD", "USDCAD", "XAUUSD", "US30", "NAS100"
]

SYMBOL_THRESHOLDS = {
    "EURUSD": 0.0030,
    "GBPUSD": 0.0040,
    "USDJPY": 0.30,
    "USDCHF": 0.0030,
    "AUDUSD": 0.0028,
    "NZDUSD": 0.0025,
    "USDCAD": 0.0025,
    "XAUUSD": 1.50,
    "US30": 25.0,
    "NAS100": 15.0
}

NEWS_API_ENABLED = False
NEWS_API_KEY = "your_api_key_here"

# === HELPERS ===

def is_valid_session():
    hour = datetime.utcnow().hour
    return 6 <= hour <= 17

def get_latest_price_data(symbol):
    base = 1.12 if "USD" in symbol else 2000
    return [base + random.uniform(-0.002, 0.002) for _ in range(5)]

def is_ranging(price_data, symbol):
    high, low = max(price_data), min(price_data)
    threshold = SYMBOL_THRESHOLDS.get(symbol.upper(), 0.003)
    return (high - low) < threshold

def broke_structure(data):
    return data[-1] > data[-2] > data[-3]

def liquidity_sweep(data):
    return abs(data[-2] - data[-3]) >= 0.0020

def fair_value_gap(data):
    return abs(data[-1] - data[-3]) > 0.0015

def determine_direction(data):
    return "buy" if data[-1] > data[-2] else "sell"

def dynamic_risk_percent(balance, total_drawdown=0.0):
    """
    Adjusts risk percent dynamically based on balance and drawdown level.
    """
    if total_drawdown > 0.20:
        return 0.005  # 0.5% risk if drawdown > 20%
    elif balance < 500:
        return 0.01  # 1% risk if balance is low
    return 0.02  # Default 2% risk

def calculate_lot(balance, risk_pct):
    risk_dollars = balance * risk_pct
    return round(risk_dollars / 100, 2)

def key_levels(symbol):
    sl = 30
    rr = 3
    tp = sl * rr
    return {"sl": sl, "tp": tp}

def news_sentiment_allows(symbol):
    if not NEWS_API_ENABLED:
        return True

    try:
        response = requests.get(
            f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API_KEY}"
        )
        data = response.json()
        headlines = " ".join([article["title"] for article in data.get("articles", [])])
        return "crash" not in headlines.lower()
    except Exception:
        return True

# === MAIN STRATEGY ===

def run_strategy(symbol, balance, total_drawdown=0.0):
    result = {
        "symbol": symbol,
        "status": "skipped",
        "reason": "",
        "trade": None,
        "details": []
    }

    if not is_valid_session():
        result["reason"] = "❌ Outside trading session"
        return result
    result["details"].append("✅ Trading session OK")

    if not news_sentiment_allows(symbol):
        result["reason"] = "❌ Negative sentiment on news"
        return result
    result["details"].append("✅ Sentiment OK")

    price_data = get_latest_price_data(symbol)

    if is_ranging(price_data, symbol):
        result["reason"] = "❌ Market is ranging"
        return result
    result["details"].append("✅ Market trending")

    if not broke_structure(price_data):
        result["reason"] = "❌ No break of structure"
        return result
    result["details"].append("✅ BOS confirmed")

    if not liquidity_sweep(price_data):
        result["reason"] = "❌ No liquidity sweep"
        return result
    result["details"].append("✅ Liquidity sweep passed")

    if not fair_value_gap(price_data):
        result["reason"] = "❌ No fair value gap"
        return result
    result["details"].append("✅ FVG confirmed")

    direction = determine_direction(price_data)
    risk_pct = dynamic_risk_percent(balance, total_drawdown)
    lot = calculate_lot(balance, risk_pct)
    levels = key_levels(symbol)

    result.update({
        "status": "trade",
        "reason": "✅ All conditions met",
        "trade": {
            "symbol": symbol,
            "direction": direction,
            "lot": lot,
            "sl": levels["sl"],
            "tp": levels["tp"]
        }
    })

    result["details"].append(f"✅ Direction: {direction.upper()}")
    result["details"].append(f"✅ Risk: {round(risk_pct*100, 2)}%, Lot: {lot}")
    result["details"].append(f"✅ SL: {levels['sl']} pips, TP: {levels['tp']} pips")

    return result

# === MULTI-SYMBOL SCAN ===

def scan_all_pairs(balance=1000, total_drawdown=0.0):
    results = []
    for symbol in SYMBOLS:
        res = run_strategy(symbol, balance, total_drawdown)
        results.append(res)
    return results

# === LOCAL TEST ===

if __name__ == "__main__":
    output = scan_all_pairs(balance=1500, total_drawdown=0.15)
    for res in output:
        print(res)
