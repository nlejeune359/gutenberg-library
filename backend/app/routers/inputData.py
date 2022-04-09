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
            tokenSet, tokenList = createTokenList(full_text_)

            # Add title & author name into token processing list
            btitle = cleanStr(book.title)
            bauthor = cleanStr(book.author_name)
            tokenSet.add(btitle)
            tokenList.append(btitle)
            tokenSet.add(bauthor)
            tokenList.append(bauthor)

            newTokenCounter = 0
            newtokenSet = []
            newTagsMapList = []

            allTagsList = session.query(Tags).filter(Tags.content.in_(tokenSet)).all()
            allTagsDict = {}

            for item in allTagsList:
                allTagsDict[item.content] = item.id
            del(allTagsList)

            for token in tokenSet:
                try:
                    tagDb = allTagsDict[token]
                except:
                    tagDb = False

                if not tagDb:
                    newTokenCounter += 1
                    tagDb = Tags(content=token, id=uuid.uuid4())
                    newtokenSet.append(tagDb)
                else:
                    tagDb = Tags(content=token, id=tagDb)

                newTagsMap = Tagmaps(book_id=newBook.id, tag_id=tagDb.id, score=tokenList.count(token))
                newTagsMapList.append(newTagsMap)

            session.bulk_save_objects(newtokenSet)
            session.bulk_save_objects(newTagsMapList)
            session.commit()

            res[book.title] = "Token detected : " + str(len(tokenSet)) + " | New token :" + str(newTokenCounter)
        else:
            res[book.title] = "Already exist"

    return res
