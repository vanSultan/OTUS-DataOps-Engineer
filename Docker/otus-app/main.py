from fastapi import FastAPI

from .database import Model, engine
from .routers import employees


Model.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(employees.router)
