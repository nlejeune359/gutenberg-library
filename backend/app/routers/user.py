from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Books, Author, Tags, Tagmaps, Users
from pydantic import BaseModel
from typing import Optional, List
from data.tokenize import createTokenList, cleanStr
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
        return {input.username: "This user already exist"}


@router.get("/getId")
async def ge_user_id(username):
    userID = session.query(Users.id).filter(Users.username == username).first()
    if userID:
        return {username: userID[0]}
    else:
        return {username: "Doesnt exist"}
