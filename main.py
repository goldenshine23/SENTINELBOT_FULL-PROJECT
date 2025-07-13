from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# === Import routers ===
from backend.auth import auth_router
from backend.users import users_router
from backend.admin import admin_router
from backend.payments import payments_router
from backend.trade import router as trade_router

app = FastAPI(
    title="Sentinel Neural-V™ Bot API",
    description="Multi-user trading API connected to MT5 via VM",
    version="1.0.0"
)

# Enable CORS (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔁 In production, use frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(payments_router, prefix="/payments", tags=["Payments"])
app.include_router(trade_router, prefix="/api", tags=["Trade"])

# Default route
@app.get("/")
def root():
    return {"message": "✅ Sentinel Neural-V API is live"}
