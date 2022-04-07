from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Books, Author, Tags, Tagmaps
from pydantic import BaseModel
from typing import Optional, List
from data.tokenize import createTokenList
import utils as u
import requests
import uuid

router = APIRouter(
            prefix="/input",
            tags=["manage", "data", "input"]
            )


db_sal = create_engine(u.db_string)
Session = sessionmaker(db_sal)
session = Session()


class Book(BaseModel):
    title: str
    author_name: str
    full_text_pointer: str


@router.post("/book")
async def input_new_books(books: List[Book]):
    res = {}
    for book in books:
        author = session.query(Author).filter(Author.author_name == book.author_name).first()

        if author is None:
            # If author doesnt exist
            author = Author(author_name=book.author_name)
            session.add(author)
            session.commit()
            session.refresh(author)

        bookAlreadyExist = session.query(Author).filter(Books.title == book.title and Books.author == author).first() is not None

        if not bookAlreadyExist:
            full_text_ = requests.get(book.full_text_pointer).text
            newBook = Books(title=book.title, full_text=full_text_, author_id=author.id)

            session.add(newBook)
            session.commit()
            session.refresh(newBook)

            # Funny part bc it's very time expensive
            tokenList = createTokenList(full_text_)

            newTokenCounter = 0
            newTokenList = []
            newTagsMapList = []

            allTagsList = session.query(Tags).filter(Tags.content.in_(tokenList)).all()
            allTagsDict = {}

            for item in allTagsList:
                allTagsDict[item.content] = item.id
            del(allTagsList)

            for token in tokenList:
                try:
                    tagDb = allTagsDict[token]
                except:
                    tagDb = False
                #tagDb = session.query(Tags).filter(Tags.content == token).first()

                if not tagDb:
                    newTokenCounter += 1
                    tagDb = Tags(content=token, id=uuid.uuid4())
                    newTokenList.append(tagDb)
                else:
                    tagDb = Tags(content=token, id=tagDb)

                    # session.add(tagDb)
                    # session.commit()
                    # session.refresh(tagDb)
                # else:
                #     tagDb = session.query(Tags).filter(Tags.content == token).first()

                newTagsMap = Tagmaps(book_id=newBook.id, tag_id=tagDb.id)
                newTagsMapList.append(newTagsMap)
                # session.add(newTagsMap)

            session.bulk_save_objects(newTokenList)
            session.bulk_save_objects(newTagsMapList)
            session.commit()
            # session.refresh(newTagsMap)

            res[book.title] = "Token detected : " + str(len(tokenList)) + " | New token :" + str(newTokenCounter)
        else:
            res[book.title] = "Already exist"

    return res
