from typing import Literal
from uuid import UUID
from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    name: str
    gender: Literal["male", "female"]
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "name": "Смирнов Иван",
                "gender": "male",
                "email": "SmirnovIV@otus.ru",
            }
        }


class EmployeeCreate(EmployeeBase):
    password: str

    class Config:
        schema_extra = {
            "example": {
                **EmployeeBase.Config.schema_extra.get("example"),
                "password": "secret",
            }
        }


class Employee(EmployeeBase):
    id: UUID

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                **EmployeeBase.Config.schema_extra.get("example"),
                "id": "1hd43a2a-c0b4-nfc4-1b33-ec2d1f1b9898",
            }
        }
