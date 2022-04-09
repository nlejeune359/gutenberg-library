from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Books, Author, Tags, Tagmaps, Historic, Users, SearchResult
from pydantic import BaseModel
from typing import Optional, List
from data.tokenize import createTokenList, cleanStr
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
        tagIDList = session.query(Tags.id).filter(Tags.content == token).all()
        resFromDBTag = session.query(Tagmaps).filter(Tagmaps.tag_id.in_(tagIDList)).all()

        histoRow = Historic(searchArgs=aij.createJSON([word]), user_id=userId)
        session.add(histoRow)
        session.commit()
        session.refresh(histoRow)

        res = []
        s_res = []
        for result in resFromDBTag:
            res.append(result.book.title)
            s_res.append(SearchResult(book_id=result.book.id, historic_id=histoRow.id))

        session.bulk_save_objects(s_res)
        session.commit()

        return res
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

        tagIDList = session.query(Tags.id).filter(Tags.content.in_(tokensList)).all()
        resFromDBTag = session.query(Tagmaps).filter(Tagmaps.tag_id.in_(tagIDList)).all()

        histoRow = Historic(searchArgs=aij.createJSON(tokensList), user_id=userId)
        session.add(histoRow)
        session.commit()
        session.refresh(histoRow)

        res = []
        s_res = []
        for result in resFromDBTag:
            if result.book.title not in res:
                res.append(result.book.title)
            s_res.append(SearchResult(book_id=result.book.id, historic_id=histoRow.id))

        session.bulk_save_objects(s_res)
        session.commit()

        return res
    else:
        raise HTTPException(status_code=400, detail=userId+" : Doesnt exist")
