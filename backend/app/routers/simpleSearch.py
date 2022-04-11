from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Books, Author, Tags, Tagmaps, Historic, Users, SearchResult
from pydantic import BaseModel
from typing import Optional, List
from data.tokenize import createTokenList, cleanStr
from algorithms.ranking import sortSearchResponse
import utils as u
import requests
import uuid
import inputArgsInJSON as aij

router = APIRouter(
            tags=["search", "simple"],
            prefix="/simple"
            )


db_sal = create_engine(u.db_string)
Session = sessionmaker(db_sal)
session = Session()


@router.get("/oneword/{word}")
async def searchOneWord(word: str, userId: str):

    try:
        uuid.UUID(userId)
    except ValueError:
        raise HTTPException(status_code=400, detail=userId+" : Doesnt exist")

    if session.query(Users).filter(Users.id == userId).count() > 0:
        token = cleanStr(word)
        resFromDBTag = session.query(Books.id, Books.title, Author.author_name).join(Author).join(Tagmaps).join(Tags).filter(Tags.content == token).distinct().all()

        res = list(map(lambda x: {"id": x.id, "title": x.title, "author_name": x.author_name}, resFromDBTag))

        s_res = []
        histoRow = Historic(id=uuid.uuid4(), searchArgs=aij.createJSON([word]), user_id=userId)
        s_res.append(histoRow)

        for result_i in range(0, len(res)):
            s_res.append(SearchResult(book_id=res[result_i]["id"], historic_id=histoRow.id))

        session.bulk_save_objects(s_res)
        session.commit()

        return sortSearchResponse(res)
    else:
        raise HTTPException(status_code=400, detail=userId+" : Doesnt exist")


@router.get("/multiplewords/{words}")
async def searchMultipleWords(words: str, userId: str):
    try:
        uuid.UUID(userId)
    except ValueError:
        raise HTTPException(status_code=400, detail=userId+" : Doesnt exist")

    if session.query(Users).filter(Users.id == userId).count() > 0:
        tokensSet, tokensList = createTokenList(words)

        # tagIDList = session.query(Tags.id).filter(Tags.content.in_(tokensList)).all()
        # resFromDBTag = session.query(Tagmaps).filter(Tagmaps.tag_id.in_(tagIDList)).all()
        resFromDBTag = session.query(Books.id, Books.title, Author.author_name).join(Author).join(Tagmaps).join(Tags).filter(Tags.content.in_(tokensList)).distinct().all()

        res = list(map(lambda x: {"id": x.id, "title": x.title, "author_name": x.author_name}, resFromDBTag))

        s_res = []
        histoRow = Historic(searchArgs=aij.createJSON(tokensList), user_id=userId)
        s_res.append(histoRow)

        for result_i in range(0, len(res)):
            s_res.append(SearchResult(book_id=res[result_i]["id"], historic_id=histoRow.id))

        session.bulk_save_objects(s_res)
        session.commit()

        return sortSearchResponse(res)
    else:
        raise HTTPException(status_code=400, detail=userId+" : Doesnt exist")
