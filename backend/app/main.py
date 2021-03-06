from fastapi import FastAPI
from sqlalchemy import create_engine
from typing import Optional, List
from data.models import Base
from routers import inputData, simpleSearch, user, advancedReasearch, books
from fastapi_cprofile.profiler import CProfileMiddleware
from fastapi.middleware.cors import CORSMiddleware
import utils as u

app = FastAPI()
#app.add_middleware(CProfileMiddleware, enable=True, server_app = app, filename='/tmp/output.pstats', strip_dirs = False, sort_by='cumulative')

# NSA security ++
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_methods=["*"],
allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    db_sal = create_engine(u.db_string)
    Base.metadata.create_all(db_sal)

app.include_router(inputData.router)
app.include_router(user.router)
app.include_router(books.router)
app.include_router(simpleSearch.router, prefix="/search")
app.include_router(advancedReasearch.router, prefix="/search")


@app.get("/")
def helloworld():
    return {"hello":"world"}
