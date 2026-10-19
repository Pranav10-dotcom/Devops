from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.database import SessionLocal
from app.database.models import Book


app = FastAPI(
    title="Library Management Platform",
    version="1.0.0"
)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home
@app.get("/")
def root():
    return {
        "message": "Library Management Platform API is running",
        "status": "success"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Database test
@app.get("/db-test")
def database_test(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))

    return {
        "status": "success",
        "message": "Database connection is working"
    }


# Create a book
@app.post("/books")
def create_book(
    title: str,
    author: str,
    isbn: str,
    db: Session = Depends(get_db)
):
    book = Book(
        title=title,
        author=author,
        isbn=isbn,
        available=True
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


# Get all books
@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


# Get a single book
@app.get("/books/{book_id}")
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        return {
            "error": "Book not found"
        }

    return book


# Update a book
@app.put("/books/{book_id}")
def update_book(
    book_id: int,
    title: str,
    author: str,
    isbn: str,
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        return {
            "error": "Book not found"
        }

    book.title = title
    book.author = author
    book.isbn = isbn

    db.commit()
    db.refresh(book)

    return book


# Delete a book
@app.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        return {
            "error": "Book not found"
        }

    db.delete(book)
    db.commit()

    return {
        "status": "success",
        "message": "Book deleted successfully"
    }
