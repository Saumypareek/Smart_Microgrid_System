from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.dependencies import get_db
from schemas.user import UserCreate, UserOut
from controllers import user_controller
from auth.auth_bearer import JWTBearer

# No global JWT protection
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Public registration endpoint
@router.post("/register", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(db, user)


# Protected endpoint
@router.get("/me", response_model=UserOut)
def read_me(current_user=Depends(user_controller.get_current_user)):
    return current_user


# Protected endpoint
@router.get("/", response_model=list[UserOut],
            dependencies=[Depends(JWTBearer())])
def read_users(db: Session = Depends(get_db)):
    return user_controller.get_users(db)


# Protected endpoint
@router.get("/{user_id}", response_model=UserOut,
            dependencies=[Depends(JWTBearer())])
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = user_controller.get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# Protected endpoint
@router.delete("/{user_id}",
                dependencies=[Depends(JWTBearer())])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not user_controller.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")

    return {"msg": "User deleted"}
