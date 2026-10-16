from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.employee import employee_router

import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app= FastAPI()

origins= [
  'http://localhost:5173',

]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_headers=['*'],
  allow_methods=['*']

)

app.include_router(employee_router, prefix='/api')