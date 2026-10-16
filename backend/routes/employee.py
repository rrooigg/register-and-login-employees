from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from dotenv import load_dotenv
import os
import bcrypt
import uuid
from jose import jwt

from models import Employee
from database import SessionLocal

employee_router= APIRouter()

load_dotenv
SECRET_KEY= os.getenv('SECRET_KEY')
ALGORITHM= 'HS256'

class RegisterRequest(BaseModel):
  name: str
  email: str
  password: str
  role: str

class LoginRequest(BaseModel):
  email: str
  password: str


@employee_router.post('/register')
def register_employee(employee: RegisterRequest):
  db= SessionLocal()
  try:
    existing_employee= db.query(Employee).filter(Employee.email == employee.email).first

    if existing_employee:
      raise HTTPException(status_code=400, detail='Employee exists already.')

    hashed_password= bcrypt.hashpw(
      employee.password.encode('utf-8'),
      bcrypt.gensalt()
    ).decode('utf-8')

    employee_id= str(uuid.uuid4())

    token= jwt.encode(
      {'employee_id': employee_id},
      SECRET_KEY,
      algorithm=ALGORITHM

    )

    new_employee= Employee(
      employee_id= employee_id,
      name= employee.name,
      email= employee.email,
      password= hashed_password,
      role= employee.role,
      token= token

    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {
      'employee_id': employee_id,
      'role': employee.role,
      'token': token

    }

  except Exception:
    db.rollback()
    raise

  finally:
    db.close()

@employee_router.post('/login')
def login_employee(employee: LoginRequest):
  db= SessionLocal()
  try:
    found_employee= db.query(Employee).filter(Employee.email == employee.email).first()

    if not found_employee or not bcrypt.checkpw(
      employee.password.encode('utf-8'),
      found_employee.password.encode('utf-8')
    ):
      raise HTTPException(status_code=400, detail='Invalid Credentials.') 

    token= jwt.encode(
      {'employee_id': found_employee.employee_id},
      SECRET_KEY,
      algorithm=ALGORITHM

    )

    return {
      'employee_id': found_employee.employee_id,
      'role': found_employee.role,
      'token': token
      
    }

  finally:
    db.close()