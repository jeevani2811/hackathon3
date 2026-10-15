from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_db
from backend.app.models import User
from backend.app.security.auth import hash_password, verify_password, create_access_token, get_current_user_optional

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "analyst"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

@router.post("/register", response_model=TokenResponse)
async def register(req: UserRegister, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.email == req.email))
    if res.scalars().first():
        raise HTTPException(status_code=400, detail="User email already registered.")

    user = User(
        email=req.email,
        hashed_password=hash_password(req.password),
        full_name=req.full_name,
        role=req.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token({"sub": user.id, "email": user.email, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email, "name": user.full_name, "role": user.role}
    }

@router.post("/login", response_model=TokenResponse)
async def login(req: UserLogin, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.email == req.email))
    user = res.scalars().first()
    if not user or not verify_password(req.password, user.hashed_password):
        # Demo friendly fallback: if demo analyst credentials used
        if req.email == "analyst@enterprise.ai" and req.password == "demo1234":
            token = create_access_token({"sub": "usr-demo-001", "email": req.email, "role": "lead_analyst"})
            return {
                "access_token": token,
                "token_type": "bearer",
                "user": {"id": "usr-demo-001", "email": req.email, "name": "Lead Strategy Analyst", "role": "lead_analyst"}
            }
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token({"sub": user.id, "email": user.email, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email, "name": user.full_name, "role": user.role}
    }

@router.get("/me")
async def current_user(user: dict = Depends(get_current_user_optional)):
    return user
