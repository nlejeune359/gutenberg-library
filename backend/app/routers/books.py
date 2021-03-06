from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Books, Author, ConsultedBooks, Tags, Tagmaps, Users
from pydantic import BaseModel
from typing import Optional, List
from data.tokenize import createTokenList, cleanStr
import utils as u
import requests
import uuid

router = APIRouter(
            prefix="/books",
            tags=["books"]
            )


db_sal = create_engine(u.db_string)
Session = sessionmaker(db_sal)
session = Session()

@router.get("/{book_id}")
async def get_book(book_id: str, userId):

    # Recuperation livre
    book = session.query(Books).filter(Books.id == book_id).first()

    if book:
    
        res = {
            'author': book.author.author_name,
            'title': book.title,
            'full_text': book.full_text
        }

        # Ecriture dans table ConsultedBooks
        consultedBook = ConsultedBooks(user_id=userId, book_id=book_id)
        session.add(consultedBook)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=400, detail="Houston we got a problem : "+str(e))

        # Reponse requete
        return res

    else:
        raise HTTPException(status_code=400, detail='book with id ' + book_id + " doesn't exist")