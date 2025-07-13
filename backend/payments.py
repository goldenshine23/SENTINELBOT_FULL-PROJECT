# backend/payments.py

from fastapi import APIRouter

payments_router = APIRouter()

# ✅ User subscription payment route (dummy for now)
@payments_router.post("/subscribe")
def subscribe():
    return {"payment": "success"}
