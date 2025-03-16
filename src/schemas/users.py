from typing import Literal

from pydantic import BaseModel, Field, EmailStr



class UserRegSchema(BaseModel):
    login: str = Field(max_length=20)
    password: str = Field(max_length=20)
    first_name: str = Field(max_length=15)
    last_name: str = Field(max_length=15)
    city: str = Field(max_length=20)
    address: str = Field(max_length=50)
    age: int = Field(ge=0, le=115)
    floor: int = Field(ge=0, le=163)
    apartament_number: int = Field(ge=0)
    data_registratsii: Literal['NOW()'] 
    status: Literal['user', 'admin']
    email: EmailStr 


class UserLoginSchema(BaseModel):
    email: EmailStr
    login: str = Field(max_length=20)
    password: str = Field(max_length=20)