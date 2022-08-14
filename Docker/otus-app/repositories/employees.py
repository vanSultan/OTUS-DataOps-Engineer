from typing import List
from uuid import UUID

from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from ..models.employee import Employee
from ..dependencies import get_db
from ..schemas.employee import EmployeeCreate


class EmployeeRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db  # произойдет внедрение зависимостей

    def find(self, uuid: UUID) -> Employee:
        query = self.db.query(Employee)
        return query.filter(Employee.id == uuid).first()

    def find_by_email(self, email: EmailStr):
        query = self.db.query(Employee)
        return query.filter(Employee.email == email).first()

    def all(self, skip: int = 0, max: int = 100) -> List[Employee]:
        query = self.db.query(Employee)
        return query.offset(skip).limit(max).all()

    def create(self, employee: EmployeeCreate) -> Employee:
        employee.password += "__you_must_hash_me"

        db_employee = Employee(**employee.dict())

        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)

        return db_employee
