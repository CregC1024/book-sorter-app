from typing import Optional
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from models import Book, BookCreate, BookListResponse, SortField, SortOrder
from services import book_service

app = FastAPI(
    title="Book Sorter API",
    description="FastAPI Backend for sorting books by Author, Title, Publisher, and ISBN",
    version="1.0.0"
)

# Enable CORS for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "Book Sorter API"}

@app.get("/api/books", response_model=BookListResponse)
def get_books(
    sort_by: SortField = Query(SortField.TITLE, description="Field to sort by: author, title, publisher, isbn"),
    sort_order: SortOrder = Query(SortOrder.ASC, description="Sort direction: asc or desc"),
    q: Optional[str] = Query(None, description="Search keyword filter across all fields")
):
    sorted_books = book_service.get_books(
        sort_by=sort_by,
        sort_order=sort_order,
        search_query=q
    )
    return BookListResponse(
        books=sorted_books,
        total=len(sorted_books),
        sort_by=sort_by,
        sort_order=sort_order,
        search_query=q
    )

@app.post("/api/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate):
    return book_service.add_book(book_in)

@app.delete("/api/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    success = book_service.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")
    return None

@app.post("/api/books/reset", response_model=dict)
def reset_books():
    book_service.reset_data()
    return {"message": "Book database reset to initial sample data", "total": len(book_service.books)}
