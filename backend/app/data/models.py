import uuid
from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint, TIMESTAMP, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
Base = declarative_base()


class Users(Base):
    """
    User is generic gutenberg-API id container.
    """
    __tablename__ = "Users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String)
    created_at = Column('created_at', TIMESTAMP(timezone=False),
                        nullable=False, default=datetime.now())


class Historic(Base):
    """
    """
    __tablename__ = "Historic"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    searchArgs = Column(JSON)
    user_id = Column(UUID(as_uuid=True), ForeignKey("Users.id"))
    created_at = Column('created_at', TIMESTAMP(timezone=False),
                        nullable=False, default=datetime.now())

    user = relationship("Users")


class Books(Base):
    __tablename__ = "Books"
    __table_args__ = ((UniqueConstraint('title', 'author_id')),)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    full_text = Column(String)
    author_id = Column(UUID(as_uuid=True), ForeignKey("Author.id"))
    created_at = Column('created_at', TIMESTAMP(timezone=False),
                        nullable=False, default=datetime.now())

    author = relationship("Author")


class ConsultedBooks(Base):
    __tablename__ = "ConsultedBooks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("Users.id"))
    book_id = Column(UUID(as_uuid=True), ForeignKey("Books.id"))
    consulted_at = Column('consulted_at', TIMESTAMP(timezone=False),
                        nullable=False, default=datetime.now())

    book = relationship("Books")
    user = relationship("Users")


class Author(Base):
    __tablename__ = "Author"
    __table_args__ = ((UniqueConstraint('author_name')),)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author_name = Column(String)
    created_at = Column('created_at', TIMESTAMP(timezone=False),
                        nullable=False, default=datetime.now())


class SearchResult(Base):
    __tablename__ = "SearchResult"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = Column(UUID(as_uuid=True), ForeignKey("Books.id"))
    historic_id = Column(UUID(as_uuid=True), ForeignKey("Historic.id"))
    created_at = Column('created_at', TIMESTAMP(timezone=False),
                        nullable=False, default=datetime.now())

    book = relationship("Books")
    historic = relationship("Historic")


class Tags(Base):
    __tablename__ = "Tags"
    __table_args__ = ((UniqueConstraint('content')),)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String)
    created_at = Column('created_at', TIMESTAMP(timezone=False),
                        nullable=False, default=datetime.now())


# MAP
class Tagmaps(Base):
    __tablename__ = "Tagmaps"
    __table_args__ = ((UniqueConstraint('book_id', 'tag_id')),)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column('timestamp', TIMESTAMP(timezone=False),
                        nullable=False, default=datetime.now())
    score = Column(Integer, default=0)
    book_id = Column(UUID(as_uuid=True), ForeignKey("Books.id"))
    tag_id = Column(UUID(as_uuid=True), ForeignKey("Tags.id"))
    book = relationship("Books")
    tag = relationship("Tags")

class Subjects(Base):
    __tablename__ = "Subjects"
    __table_args__ = ((UniqueConstraint('content')),)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String)
    created_at = Column('created_at', TIMESTAMP(timezone=False),
                        nullable=False, default=datetime.now())


# MAP
class SubjectMaps(Base):
    __tablename__ = "SubjectMaps"
    __table_args__ = ((UniqueConstraint('book_id', 'subject_id')),)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column('timestamp', TIMESTAMP(timezone=False),
                        nullable=False, default=datetime.now())
    book_id = Column(UUID(as_uuid=True), ForeignKey("Books.id"))
    subject_id = Column(UUID(as_uuid=True), ForeignKey("Subjects.id"))
    book = relationship("Books")
    subject = relationship("Subjects")