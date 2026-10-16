from sqlalchemy import Column, String
from database import Base

class Employee(Base):
  __tablename__= 'employees'

  employee_id= Column(String, primary_key=True, index=True)
  name= Column(String,nullable=False)
  email= Column(String, nullable=False, unique=True, index=True)
  password= Column(String, nullable=False)
  role= Column(String, nullable=False)
  token= Column(String, nullable=True)