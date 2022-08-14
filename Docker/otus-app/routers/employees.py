from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import parse_obj_as
from typing import List
from uuid import UUID

from ..schemas.employee import Employee, EmployeeCreate
from ..repositories.employees import EmployeeRepository


router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=List[Employee])
def list_employees(
    skip: int = 0, max: int = 10, employees: EmployeeRepository = Depends()
):
    db_employees = employees.all(skip=skip, max=max)
    return parse_obj_as(List[Employee], db_employees)


@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
def store_employee(
    employee: EmployeeCreate, employees: EmployeeRepository = Depends()
):
    db_employee = employees.find_by_email(email=employee.email)

    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_employee = employees.create(employee)
    return Employee.from_orm(db_employee)


@router.get("/{employee_id}", response_model=Employee)
def get_employee(employee_id: UUID, employees: EmployeeRepository = Depends()):
    db_employee = employees.find(employee_id)

    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return Employee.from_orm(db_employee)
