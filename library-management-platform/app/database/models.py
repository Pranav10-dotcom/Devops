from sqlalchemy import Column, Integer, String, Boolean
from app.database.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(200), nullable=False)
    isbn = Column(String(50), unique=True, nullable=False)
    available = Column(Boolean, default=True)
