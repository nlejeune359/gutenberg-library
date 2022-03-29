from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Base

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    db_string = "postgresql://postgres:example@database:5432/gutenberg"
    db_sal = create_engine(db_string)
    Session = sessionmaker(db_sal)
    session = Session()
    Base.metadata.create_all(db_sal)

@app.get("/")
def helloworld():
    return {"hello":"world"}
