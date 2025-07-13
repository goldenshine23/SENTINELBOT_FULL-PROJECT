import time
from datetime import datetime
from vm.MT5Bridge import connect, place_order
from backend.strategy import run_strategy
import json, os

# === Load watchlist ===
WATCHLIST_FILE = os.path.join(os.path.dirname(__file__), "watchlist.json")
with open(WATCHLIST_FILE, "r") as f:
    WATCHLIST = json.load(f)

def run_bot():
    print("🤖 Sentinel Bot auto-run started.")
    connect()

    while True:
        print(f"\n🕒 Scanning @ {datetime.utcnow()}")

        for symbol in WATCHLIST:
            balance = 1000  # Placeholder, ideally pull real balance from account
            result = run_strategy(symbol, balance)

            if result["status"] == "trade":
                trade = result["trade"]
                print(f"🚀 Executing trade: {trade}")
                response = place_order(
                    symbol=trade["symbol"],
                    direction=trade["direction"],
                    lot=trade["lot"],
                    sl=trade["sl"],
                    tp=trade["tp"]
                )
                print(f"✅ Order result: {response}")
            else:
                print(f"⏭️ {symbol}: {result['reason']}")

        time.sleep(60)  # wait before next scan

if __name__ == "__main__":
    run_bot()
from vm.telegram_notify import send_alert
