from fastapi import FastAPI
from sqlalchemy import create_engine
from typing import Optional, List
from data.models import Base
from routers import inputData
import utils as u
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    db_sal = create_engine(u.db_string)
    Base.metadata.create_all(db_sal)

app.include_router(inputData.router)

@app.get("/")
def helloworld():
    return {"hello":"world"}
