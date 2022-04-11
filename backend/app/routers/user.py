from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Books, Author, ConsultedBooks, Tags, Tagmaps, Users, Subjects, SubjectMaps
from pydantic import BaseModel
from typing import Optional, List
from data.tokenize import createTokenList, cleanStr
from algorithms.jaccard import computeJaccardIndex
import utils as u
import requests
import uuid

router = APIRouter(
            prefix="/user",
            tags=["manage", "user"]
            )


db_sal = create_engine(u.db_string)
Session = sessionmaker(db_sal)
session = Session()


class newUser(BaseModel):
    username: str


@router.post("/create")
async def create_user(input: newUser):
    if session.query(Users).filter(Users.username == input.username).count() < 1:
        user = Users(username=input.username)
        session.add(user)
        session.commit()
        return {input.username: user.id}
    else:
        raise HTTPException(status_code=400, detail=input.username+"This user already exist")


@router.get("/getId")
async def ge_user_id(username):
    userID = session.query(Users.id).filter(Users.username == username).first()
    if userID:
        return {username: userID[0]}
    else:
        raise HTTPException(status_code=400, detail=username+" : Doesnt exist")

@router.get("/suggestions")
async def get_history(userId):
    request = session.query(ConsultedBooks.book_id).filter(
        ConsultedBooks.user_id == userId).order_by(ConsultedBooks.consulted_at.desc()).limit(5).all()
    
    subjectMapsFromDB = session.query(SubjectMaps.book_id, SubjectMaps.subject_id).all()
    # {'book_id': ['subject_id']}

    request = list(map(lambda x: x[0], request))
    setADict: list[str] = []
    setBDict = {}

    for sub in subjectMapsFromDB:

        if sub.book_id in request:
            # setA
            if sub.subject_id not in setADict:
                setADict.append(sub.subject_id)

        else:
            # setB
            if sub.book_id in setBDict:
                setBDict[sub.book_id].append(sub.subject_id)
            else:
                setBDict[sub.book_id] = [sub.subject_id]

    resBDict ={}
    for bookID in setBDict:
        resBDict[bookID] = computeJaccardIndex(setADict, setBDict[bookID])

    resBDict = sorted(resBDict.items(), key=lambda x:x[1], reverse=True)

    books_id = []
    for (key, value) in resBDict:
        if value == 0:
            break
        books_id.append(key)

    res = session.query(Books.id, Books.title, Author.author_name).join(Author).filter(Books.id.in_(books_id)).limit(10).all()

    resDict = []
    for item in res:
        resDict.append({'book_id': item.id, 'title': item.title, 'author': item.author_name})

    return resDict