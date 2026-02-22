from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import pytz
import random
import os

try:
    from .database import engine, SessionLocal
    from .models import Base, User, SupportQuery, PasswordResetCode
    from .schemas import (
        UserSignup,
        UserLogin,
        SupportQueryCreate,
        ForgotPasswordRequest,
        ResetPasswordRequest,
    )
    from .scheduler import start_scheduler
    from .leetcode_checker import get_last_submission_date
    from .email_utils import send_email
except ImportError:
    from database import engine, SessionLocal
    from models import Base, User, SupportQuery, PasswordResetCode
    from schemas import (
        UserSignup,
        UserLogin,
        SupportQueryCreate,
        ForgotPasswordRequest,
        ResetPasswordRequest,
    )
    from scheduler import start_scheduler
    from leetcode_checker import get_last_submission_date
    from email_utils import send_email

# ---------------- APP INIT ----------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://streak-forge-33fu.vercel.app","http://localhost:3000,http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# ---------------- DB ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- PASSWORD ----------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ---------------- JWT ----------------
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey_change_this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# ---------------- ROUTES ----------------

@app.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        password=hash_password(user.password),
        leetcode_username=user.leetcode_username,
        timezone=user.timezone
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    email = user.email.lower().strip()
    db_user = db.query(User).filter(User.email == email).first()

    print("Entered password:", user.password)
    print("Stored hash:", db_user.password if db_user else "No user")

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    result = verify_password(user.password, db_user.password)
    print("Verify result:", result)

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/")
def health():
    return {"status":"alive"}

@app.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "leetcode_username": current_user.leetcode_username,
        "timezone": current_user.timezone
    }

@app.get("/dashboard")
def dashboard(current_user: User = Depends(get_current_user)):

    tz = pytz.timezone(current_user.timezone)
    now_local = datetime.now(tz)

    last_submission = get_last_submission_date(
        current_user.leetcode_username,
        current_user.timezone
    )

    solved_today = False
    last_submission_display = None

    if last_submission:
        solved_today = last_submission.date() == now_local.date()
        last_submission_display = last_submission.strftime("%d %b %Y, %I:%M %p %Z")

    reminder_sent_today = False

    if current_user.last_reminder_sent:
        last_sent_local = current_user.last_reminder_sent.astimezone(tz)
        reminder_sent_today = last_sent_local.date() == now_local.date()

    return {
        "email": current_user.email,
        "today_status": "Completed ✅" if solved_today else "Not Completed ❌",
        "last_submission_date": last_submission_display,
        "reminder_sent": reminder_sent_today
    }


@app.post("/support-query")
def create_support_query(payload: SupportQueryCreate, db: Session = Depends(get_db)):
    support_query = SupportQuery(
        name=payload.name.strip(),
        email=payload.email.lower().strip(),
        message=payload.message.strip(),
    )

    db.add(support_query)
    db.commit()

    return {"message": "Support query submitted successfully"}


@app.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"message": "If this email exists, a reset code has been sent"}

    code = f"{random.randint(100000, 999999)}"
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    reset_code = PasswordResetCode(
        email=email,
        code=code,
        expires_at=expires_at,
        used=0,
    )
    db.add(reset_code)
    db.commit()

    subject = "StreakForge Password Reset Code"
    body = (
        f"Hello,\n\n"
        f"Your StreakForge password reset code is: {code}\n"
        f"This code will expire in 10 minutes.\n\n"
        f"If you did not request this, please ignore this email.\n"
    )

    try:
        send_email(to_email=email, subject=subject, body=body)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to send reset code email")

    return {"message": "Reset code sent to your email"}


@app.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    code = payload.code.strip()
    new_password = payload.new_password.strip()

    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_entry = (
        db.query(PasswordResetCode)
        .filter(
            PasswordResetCode.email == email,
            PasswordResetCode.code == code,
            PasswordResetCode.used == 0,
        )
        .order_by(PasswordResetCode.created_at.desc())
        .first()
    )

    if not reset_entry:
        raise HTTPException(status_code=400, detail="Invalid reset code")

    if datetime.utcnow() > reset_entry.expires_at:
        raise HTTPException(status_code=400, detail="Reset code has expired")

    user.password = hash_password(new_password)
    reset_entry.used = 1

    db.commit()

    return {"message": "Password reset successful"}


@app.delete("/delete-account")
def delete_account(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    email = current_user.email

    db.query(PasswordResetCode).filter(PasswordResetCode.email == email).delete()
    db.query(SupportQuery).filter(SupportQuery.email == email).delete()
    db.delete(current_user)
    db.commit()

    return {"message": "Account deleted permanently"}

# ---------------- START SCHEDULER ----------------
start_scheduler()
