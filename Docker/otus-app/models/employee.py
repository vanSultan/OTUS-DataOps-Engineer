from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from ..database import Model


class Employee(Model):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    gender = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
