from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.user import UserCreate, UserLogin
from controllers import user_controller
from auth.auth_handler import verify_password, encode_jwt
from database.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_controller.get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return user_controller.create_user(db, user)


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = user_controller.get_user_by_email(db, user.email)

    if not db_user or not verify_password(
        user.password, str(db_user.password)
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = encode_jwt(db_user.user_id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
