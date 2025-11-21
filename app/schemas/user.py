from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    is_active: bool | None = None
    role: str | None = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str
    
    class Config:
        from_attributes = True