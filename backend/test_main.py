from fastapi.testclient import TestClient
from main import app
from services import book_service

client = TestClient(app)

def setup_function():
    """Reset data before each test."""
    book_service.reset_data()

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_sort_by_title_asc():
    response = client.get("/api/books?sort_by=title&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    titles = [b["title"] for b in data["books"]]
    # Clean Code, Code Complete, Designing Data-Intensive..., Domain-Driven..., Introduction to Algorithms, Refactoring, Structure..., The Pragmatic..., You Don't Know JS...
    assert titles == sorted(titles, key=lambda t: t.replace("The ", "").replace("A ", "").lower())

def test_sort_by_author_asc():
    response = client.get("/api/books?sort_by=author&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    authors = [b["author"] for b in data["books"]]
    assert len(authors) > 0

def test_sort_by_publisher_asc():
    response = client.get("/api/books?sort_by=publisher&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    publishers = [b["publisher"] for b in data["books"]]
    assert publishers == sorted(publishers, key=lambda p: p.lower())

def test_sort_by_publisher_desc():
    response = client.get("/api/books?sort_by=publisher&sort_order=desc")
    assert response.status_code == 200
    data = response.json()
    publishers = [b["publisher"] for b in data["books"]]
    assert publishers == sorted(publishers, key=lambda p: p.lower(), reverse=True)

def test_sort_by_isbn():
    response = client.get("/api/books?sort_by=isbn&sort_order=asc")
    assert response.status_code == 200
    data = response.json()
    isbns = [b["clean_isbn"] for b in data["books"]]
    assert isbns == sorted(isbns)

def test_search_filter():
    response = client.get("/api/books?q=Prentice")
    assert response.status_code == 200
    data = response.json()
    assert len(data["books"]) == 1
    assert data["books"][0]["publisher"] == "Prentice Hall"

def test_create_and_delete_book():
    new_book = {
        "title": "Modern Angular Architecture",
        "author": "Jane Developer",
        "publisher": "Tech Press",
        "isbn": "978-1234567890"
    }
    create_res = client.post("/api/books", json=new_book)
    assert create_res.status_code == 201
    created = create_res.json()
    assert created["id"] is not None
    assert created["title"] == "Modern Angular Architecture"

    # Delete book
    del_res = client.delete(f"/api/books/{created['id']}")
    assert del_res.status_code == 204
