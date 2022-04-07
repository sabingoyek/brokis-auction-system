from typing import Optional, List, TYPE_CHECKING


from pydantic import BaseModel, EmailStr

from .auction import Auction

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    email: str
    is_active: Optional[bool]

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    auctions: List[Auction] = []


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
