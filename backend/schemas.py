from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ---------------- SIGNUP ----------------
class UserSignup(BaseModel):
    email: EmailStr
    password: str
    leetcode_username: str
    timezone: str


# ---------------- LOGIN ----------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ---------------- DASHBOARD RESPONSE ----------------
class DashboardResponse(BaseModel):
    email: str
    current_streak: int
    longest_streak: int
    last_submission_date: Optional[str]
