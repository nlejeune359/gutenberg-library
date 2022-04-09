from fastapi import FastAPI
from sqlalchemy import create_engine
from typing import Optional, List
from data.models import Base
from routers import inputData, simpleSearch
from fastapi_cprofile.profiler import CProfileMiddleware
import utils as u

app = FastAPI()
app.add_middleware(CProfileMiddleware, enable=True, server_app = app, filename='/tmp/output.pstats', strip_dirs = False, sort_by='cumulative')


@app.on_event("startup")
async def startup_event():
    db_sal = create_engine(u.db_string)
    Base.metadata.create_all(db_sal)

app.include_router(inputData.router)
app.include_router(simpleSearch.router, prefix="/search")

@app.get("/")
def helloworld():
    return {"hello":"world"}
