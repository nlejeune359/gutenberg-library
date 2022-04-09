from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Books, Author, Tags, Tagmaps
from pydantic import BaseModel
from typing import Optional, List
from data.tokenize import createTokenList, cleanStr
import utils as u
import requests
import uuid

router = APIRouter(
            tags=["search", "simple"]
            )


db_sal = create_engine(u.db_string)
Session = sessionmaker(db_sal)
session = Session()


@router.get("/simple/{word}")
async def searchOneWord(word: str, userId: str):

    token = cleanStr(word)
    tagIDList = session.query(Tags.id).filter(Tags.content == token).all()
    resFromDBTag = session.query(Tagmaps).filter(Tagmaps.tag_id.in_(tagIDList)).all()

    res = []
    for result in resFromDBTag:
        res.append(result.book.title)

    return res
