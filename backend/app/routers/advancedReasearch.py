from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from data.models import Books, Author, Tags, Tagmaps, Historic, Users, SearchResult
from pydantic import BaseModel
from typing import Optional, List
from data.tokenize import createTokenList, cleanStr
from algorithms.ranking import sortSearchResponse
import inputArgsInJSON as aij
import utils as u
import requests
import uuid


router = APIRouter(
            prefix="/avanced",
            tags=["search", "advanced"]
            )


db_sal = create_engine(u.db_string)
Session = sessionmaker(db_sal)
session = Session()


@router.get("/token/{regex}")
async def searchOnToken(regex: str, userId: str):
    try:
        uuid.UUID(userId)
    except ValueError:
        raise HTTPException(status_code=400, detail=userId+" : Doesnt exist")

    if session.query(Users).filter(Users.id == userId).count() > 0:

        try:
            resFromDBTag = session.query(Books.id, Books.title, Author.author_name).join(Author).join(Tagmaps).join(Tags).filter(Tags.content.op('~*')(regex)).distinct().all()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Research error :" + str(e))

        res = list(map(lambda x: {"id": x.id, "title": x.title, "author_name": x.author_name}, resFromDBTag))

        s_res = []
        histoRow = Historic(id=uuid.uuid4(), searchArgs=aij.createJSON([regex]), user_id=userId)
        s_res.append(histoRow)

        for result_i in range(0, len(res)):
            s_res.append(SearchResult(book_id=res[result_i]["id"], historic_id=histoRow.id))
        session.bulk_save_objects(s_res)
        session.commit()

        return sortSearchResponse(res)
    else:
        raise HTTPException(status_code=400, detail=userId+" : Doesnt exist")


@router.get("/fulltext/{regex}")
async def searchOnFullText(regex: str, userId: str):
    try:
        uuid.UUID(userId)
    except ValueError:
        raise HTTPException(status_code=400, detail=userId+" : Doesnt exist")

    if session.query(Users).filter(Users.id == userId).count() > 0:

        try:
            # resFromDBTag = session.query(Tagmaps.book).join(Tags).filter(Tags.content.op('~*')(regex)).all()
            resFromFulltext = session.query(Books.id, Books.title, Author.author_name).join(Author).filter(Books.full_text.op('~*')(regex)).all()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Research error :" + str(e))

        res = list(map(lambda x: {"id": x.id, "title": x.title, "author_name": x.author_name}, resFromFulltext))

        s_res = []
        histoRow = Historic(id=uuid.uuid4(), searchArgs=aij.createJSON([regex]), user_id=userId)
        s_res.append(histoRow)

        for result_i in range(0, len(res)):
            s_res.append(SearchResult(book_id=res[result_i]["id"], historic_id=histoRow.id))
        session.bulk_save_objects(s_res)
        session.commit()

        return sortSearchResponse(res)
    else:
        raise HTTPException(status_code=400, detail=userId+" : Doesnt exist")
