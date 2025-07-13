# backend/auth.py

from fastapi import APIRouter

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth_router.post("/register")
def register():
    return {"message": "Registered"}

@auth_router.post("/login")
def login():
    return {"message": "Logged in"}
