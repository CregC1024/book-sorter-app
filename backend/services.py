import re
from typing import List, Optional
from models import Book, BookCreate, SortField, SortOrder

def normalize_isbn(isbn_str: str) -> str:
    """Extract numbers and trailing 'X' from ISBN for uniform comparison."""
    cleaned = re.sub(r'[^0-9X]', '', isbn_str.upper())
    return cleaned

INITIAL_BOOKS: List[dict] = [
    {
        "id": 1,
        "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
        "author": "Robert C. Martin",
        "publisher": "Prentice Hall",
        "isbn": "978-0132350884"
    },
    {
        "id": 2,
        "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
        "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
        "publisher": "Addison-Wesley",
        "isbn": "978-0201633610"
    },
    {
        "id": 3,
        "title": "The Pragmatic Programmer: Your Journey To Mastery",
        "author": "Andrew Hunt, David Thomas",
        "publisher": "Addison-Wesley Professional",
        "isbn": "978-0135957059"
    },
    {
        "id": 4,
        "title": "Structure and Interpretation of Computer Programs",
        "author": "Harold Abelson, Gerald Jay Sussman",
        "publisher": "MIT Press",
        "isbn": "978-0262510875"
    },
    {
        "id": 5,
        "title": "Refactoring: Improving the Design of Existing Code",
        "author": "Martin Fowler",
        "publisher": "Addison-Wesley",
        "isbn": "978-0201485677"
    },
    {
        "id": 6,
        "title": "Code Complete: A Practical Handbook of Software Construction",
        "author": "Steve McConnell",
        "publisher": "Microsoft Press",
        "isbn": "978-0735619678"
    },
    {
        "id": 7,
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein",
        "publisher": "MIT Press",
        "isbn": "978-0262033848"
    },
    {
        "id": 8,
        "title": "You Don't Know JS Yet: Get Started",
        "author": "Kyle Simpson",
        "publisher": "Independently published",
        "isbn": "979-8650350828"
    },
    {
        "id": 9,
        "title": "Domain-Driven Design: Tackling Complexity in the Heart of Software",
        "author": "Eric Evans",
        "publisher": "Addison-Wesley",
        "isbn": "978-0321125217"
    },
    {
        "id": 10,
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
        "publisher": "O'Reilly Media",
        "isbn": "978-1449373320"
    }
]

class BookService:
    def __init__(self):
        self.books: List[Book] = []
        self.next_id = 1
        self.reset_data()

    def reset_data(self):
        self.books = []
        self.next_id = 1
        for item in INITIAL_BOOKS:
            book = Book(
                id=item["id"],
                title=item["title"],
                author=item["author"],
                publisher=item["publisher"],
                isbn=item["isbn"],
                clean_isbn=normalize_isbn(item["isbn"])
            )
            self.books.append(book)
            if item["id"] >= self.next_id:
                self.next_id = item["id"] + 1

    def get_books(
        self,
        sort_by: SortField = SortField.TITLE,
        sort_order: SortOrder = SortOrder.ASC,
        search_query: Optional[str] = None
    ) -> List[Book]:
        filtered = self.books

        if search_query:
            q = search_query.lower().strip()
            filtered = [
                b for b in filtered
                if q in b.title.lower()
                or q in b.author.lower()
                or q in b.publisher.lower()
                or q in b.isbn.lower()
            ]

        def get_sort_key(book: Book):
            if sort_by == SortField.TITLE:
                # Ignore leading "A ", "An ", "The " for title sorting if desired, or standard lower title
                title_clean = re.sub(r'^(the|a|an)\s+', '', book.title, flags=re.IGNORECASE)
                return title_clean.lower()
            elif sort_by == SortField.AUTHOR:
                # Primary sort by last name of first author, secondary full author string
                first_author = book.author.split(',')[0].strip()
                name_parts = first_author.split()
                last_name = name_parts[-1].lower() if name_parts else ""
                return (last_name, book.author.lower())
            elif sort_by == SortField.PUBLISHER:
                return book.publisher.lower()
            elif sort_by == SortField.ISBN:
                return book.clean_isbn
            return book.id

        is_descending = (sort_order == SortOrder.DESC)
        sorted_books = sorted(filtered, key=get_sort_key, reverse=is_descending)
        return sorted_books

    def add_book(self, book_in: BookCreate) -> Book:
        new_book = Book(
            id=self.next_id,
            title=book_in.title.strip(),
            author=book_in.author.strip(),
            publisher=book_in.publisher.strip(),
            isbn=book_in.isbn.strip(),
            clean_isbn=normalize_isbn(book_in.isbn)
        )
        self.next_id += 1
        self.books.append(new_book)
        return new_book

    def delete_book(self, book_id: int) -> bool:
        initial_len = len(self.books)
        self.books = [b for b in self.books if b.id != book_id]
        return len(self.books) < initial_len

book_service = BookService()
