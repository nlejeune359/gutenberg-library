from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.models import Books, Author, Tags, Tagmaps, SubjectMaps, Subjects
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
    subjects: List[str]


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

        bookAlreadyExist = session.query(Author.id).filter(Books.title == book.title and Books.author == author).first() is not None

        if not bookAlreadyExist:
            full_text_ = requests.get(book.full_text_pointer).text
            newBook = Books(title=book.title, full_text=full_text_, author_id=author.id)

            session.add(newBook)
            try:
                session.commit()
            except Exception as e:
                res[book.title] = "Error detected :" + str(e)
                session.rollback()
                continue

            session.refresh(newBook)

            # Subjects
            subjectSet = set()
            for subjectItem in book.subjects:
                subjectSet_, subjectsListBis = createTokenList(subjectItem)
                del(subjectsListBis)
                subjectSet = subjectSet.union(subjectSet_)

            newSubjectSet = []
            newSubjectMapsList = []

            allSubjectsList = session.query(Subjects).filter(Subjects.content.in_(subjectSet)).all()
            allSubjectsDict = {}

            for item in allSubjectsList:
                allSubjectsDict[item.content] = item.id
            del(allSubjectsList)

            for subject in subjectSet:
                if subject in allSubjectsDict:
                    subjectDb = allSubjectsDict[subject]
                else:
                    subjectDb = False

                # try:
                #     subjectDb = allSubjectsDict[subject]
                # except:
                #     subjectDb = False

                if not subjectDb:
                    subjectDb = Subjects(content=subject, id=uuid.uuid4())
                    newSubjectSet.append(subjectDb)
                else:
                    subjectDb = Subjects(content=subject, id=subjectDb)

                newSubjectMap = SubjectMaps(book_id=newBook.id, subject_id=subjectDb.id)
                newSubjectMapsList.append(newSubjectMap)


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

            allTagsList = session.query(Tags.id, Tags.content).filter(Tags.content.in_(tokenSet)).all()
            allTagsDict = {}

            for item in allTagsList:
                allTagsDict[item.content] = item.id
            del(allTagsList)

            for token in tokenSet:
                if token in allTagsDict:
                    tagDb = allTagsDict[token]
                else:
                    tagDb = False
                # try:
                #     tagDb = allTagsDict[token]
                # except:
                #     tagDb = False

                if not tagDb:
                    newTokenCounter += 1
                    tagDb = Tags(content=token, id=uuid.uuid4())
                    newtokenSet.append(tagDb)
                else:
                    tagDb = Tags(content=token, id=tagDb)

                newTagsMap = Tagmaps(book_id=newBook.id, tag_id=tagDb.id)
                newTagsMapList.append(newTagsMap)

            session.bulk_save_objects(newtokenSet)
            session.bulk_save_objects(newSubjectSet)
            session.bulk_save_objects(newSubjectMapsList)
            session.bulk_save_objects(newTagsMapList)
            try:
                session.commit()
                res[book.title] = "Token detected : " + str(len(tokenSet)) + " | New token :" + str(newTokenCounter)
            except Exception as e:
                session.rollback()
                res[book.title] = "Error detected :" + str(e)

        else:
            res[book.title] = "Already exist"

    return res
