from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
from backend.strategy import run_strategy
from vm.MT5Bridge import place_order

router = APIRouter()

class TradeRequest(BaseModel):
    symbols: List[str]
    balance: float
    login: int
    server: str
    password: str

@router.post("/scan")
def scan_and_trade(data: TradeRequest):
    results = []

    for symbol in data.symbols:
        result = run_strategy(symbol, data.balance)

        if result["status"] == "trade":
            trade = result["trade"]

            try:
                mt5_result = place_order(
                    symbol=trade["symbol"],
                    direction=trade["direction"],
                    lot=trade["lot"],
                    sl=trade["sl"],
                    tp=trade["tp"],
                    login=data.login,
                    server=data.server,
                    password=data.password
                )
                result["mt5_response"] = (
                    mt5_result._asdict() if hasattr(mt5_result, "_asdict") else str(mt5_result)
                )
            except Exception as e:
                result["mt5_response"] = {"error": str(e)}

        results.append(result)

    has_trade = any(r["status"] == "trade" for r in results)

    return {
        "status": "trade_found" if has_trade else "no_signal",
        "timestamp": datetime.utcnow(),
        "results": results
    }
