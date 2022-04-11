from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy import create_engine, or_
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


def getBooksAndAuthorAlreadyInDb(books):
    booksTitles = list(map(lambda x: x.title, books))
    booksAuthor_name = list(map(lambda x: x.author_name, books))
    statement = session.query(Books.title, Author.author_name, Author.id).join(Author).filter(or_(Books.title.in_(booksTitles), Author.author_name.in_(booksAuthor_name)))
    booksInDB = statement.all()
    authorRes = set()
    booksTitleRes = set()
    for b in booksInDB:
        authorRes.add((b.author_name, b.id))
        booksTitleRes.add(b.title)
    return booksTitleRes, authorRes


def deleteBookAlreadyInDB(books, booksTitleAIDB):

    booksTitlesInDB = set()
    for book in booksTitleAIDB:
        booksTitlesInDB.add(book)

    res = []
    for b in books:
        if b.title not in booksTitlesInDB:
            res.append(b)
    return res


def getAuthorMap(books, authorAIDB):
    # Author
    newAuthor = set()
    resMap = dict()

    authorID = dict()
    for a in authorAIDB:
        authorID[a[0]] = a[1]

    for book in books:
        if book.author_name in authorID:
            resMap[book.title] = authorID[book.author_name]
        else:
            idA = uuid.uuid4()
            resMap[book.title] = idA
            authorID[book.author_name] = idA
            author = Author(id=idA, author_name=book.author_name)
            newAuthor.add(author)
    session.bulk_save_objects(newAuthor)

    return resMap


def addNewbooks(books, authorsMap):
    newBooks = []
    allNewTags = []
    allNewTagsMaps = []
    booksMap = dict()
    tagMap = dict()

    for book in books:
        idB = uuid.uuid4()
        booksMap[book.title] = idB
        full_text_ = requests.get(book.full_text_pointer).text
        b = Books(id=idB,
                title=book.title,
                author_id=authorsMap[book.title],
                full_text=full_text_)
        newTags, newTagsMaps, tagMap = manageTags(full_text_, idB, tagMap)
        allNewTags = allNewTags + newTags
        allNewTagsMaps = allNewTagsMaps + newTagsMaps
        newBooks.append(b)

    session.bulk_save_objects(newBooks)
    session.bulk_save_objects(allNewTags)
    session.bulk_save_objects(allNewTagsMaps)

    return booksMap


def manageTags(fulltext, bookID, tagMap):
    tagsSet_, tagsList_ = createTokenList(fulltext)
    if not tagMap:
        TagsInDB = session.query(Tags.id, Tags.content).filter(Tags.content.in_(tagsSet_)).all()

        #tagMap = dict()
        for t in TagsInDB:
            tagMap[t.content] = t.id

    newTags = []
    for tag in tagsSet_:
        if tag not in tagMap:
            idT = uuid.uuid4()
            tagMap[tag] = idT
            s = Tags(id=idT, content=tag)
            newTags.append(s)

    newTagsMaps = []
    tagsAlreadyTreated = []
    for tag in tagsSet_:
        if tagMap[tag] not in tagsAlreadyTreated:
            tagsAlreadyTreated.append(tagMap[tag])
            newTagsMaps.append(Tagmaps(book_id=bookID, tag_id=tagMap[tag]))
    # session.bulk_save_objects(newTags)
    # session.bulk_save_objects(newTagsMaps)
    return newTags, newTagsMaps, tagMap


def manageSubjects(books, booksMap):
    allSubjectsInInput = set()
    for book in books:
        tmpL = set()
        for subject in book.subjects:
            settmp, listtmp = createTokenList(subject)
            tmpL = tmpL.union(settmp)
        allSubjectsInInput = allSubjectsInInput.union(tmpL)

    subjectsInDB = session.query(Subjects.id, Subjects.content).filter(Subjects.content.in_(allSubjectsInInput)).all()

    subMaps = dict()
    for s in subjectsInDB:
        subMaps[s.content] = s.id

    newSubs = []
    for sub in allSubjectsInInput:
        if sub not in subMaps:
            idS = uuid.uuid4()
            subMaps[sub] = idS
            s = Subjects(id=idS, content=sub)
            newSubs.append(s)

    newSubMaps = []
    subAlreadyTreated = []
    for book in books:
        for subInBooks in book.subjects:
            subIBset_, subIBlist_ = createTokenList(subInBooks)
            for item in subIBset_:
                if subMaps[item] not in subAlreadyTreated:
                    subAlreadyTreated.append(subMaps[item])
                    newSubMaps.append(SubjectMaps(book_id=booksMap[book.title], subject_id=subMaps[item]))
    session.bulk_save_objects(newSubs)
    session.bulk_save_objects(newSubMaps)
    return subMaps


@router.post("/book")
async def input_new_books(books: List[Book]):

    booksTitleAIDB, authorAIDB = getBooksAndAuthorAlreadyInDb(books)
    books = deleteBookAlreadyInDB(books, booksTitleAIDB)
    authorsMap = getAuthorMap(books, authorAIDB)
    booksMap = addNewbooks(books, authorsMap)
    subMaps = manageSubjects(books, booksMap)
    session.commit()
    return books
