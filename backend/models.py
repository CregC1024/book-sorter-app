from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class SortField(str, Enum):
    TITLE = "title"
    AUTHOR = "author"
    PUBLISHER = "publisher"
    ISBN = "isbn"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, description="Book title")
    author: str = Field(..., min_length=1, description="Book author name")
    publisher: str = Field(..., min_length=1, description="Publisher name")
    isbn: str = Field(..., min_length=9, description="ISBN-10 or ISBN-13 identifier")

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    clean_isbn: str = Field(..., description="Normalized ISBN digits for accurate numeric sorting")

class BookListResponse(BaseModel):
    books: list[Book]
    total: int
    sort_by: SortField
    sort_order: SortOrder
    search_query: Optional[str] = None
