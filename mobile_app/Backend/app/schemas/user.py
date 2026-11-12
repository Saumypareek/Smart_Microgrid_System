from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int = Field(..., alias="user_id")
    name: str
    email: EmailStr

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
