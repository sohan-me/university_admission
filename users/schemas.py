from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: bool = False


class UserUpdate(BaseModel):
    is_verified: bool = False


class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool
    is_verified: bool

    class Config:
        orm_mode = True


class UserResponseToken(BaseModel):
    user: UserResponse
    token: Token




class UserProfileBase(BaseModel):
    full_name: str
    phone: str
    whatsapp: str
    address: str
    occupation: str
    experience: bool
    exp_description: Optional[str] = None
    initial_refffer: str
    no_of_deal: int = 0
    office: bool = False
    office_address: Optional[str] = None
    student_country: str
    student_destination_country: str
    special_service: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    address: Optional[str] = None
    occupation: Optional[str] = None
    experience: Optional[bool] = None
    exp_description: Optional[str] = None
    initial_refffer: Optional[str] = None
    no_of_deal: Optional[int] = None
    office: Optional[bool] = None
    office_address: Optional[str] = None
    student_country: Optional[str] = None
    student_destination_country: Optional[str] = None
    special_service: Optional[str] = None




class UserProfileResponse(UserProfileBase):
    id: int
    nid_passport_file: Optional[str] = None

    class Config:
        orm_mode = True


