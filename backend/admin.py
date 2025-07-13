# backend/admin.py

from fastapi import APIRouter

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@admin_router.get("/dashboard")
def admin_dashboard():
    return {"admin": "control panel"}
# backend/admin.py

from fastapi import APIRouter

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@admin_router.get("/dashboard")
def admin_dashboard():
    return {"admin": "control panel"}
