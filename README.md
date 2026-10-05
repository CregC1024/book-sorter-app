# Book Sorter Web Application (Angular + Python FastAPI)

A modern full-stack web application designed to manage and sort a book library by **Author**, **Title**, **Publisher**, and **ISBN number**.

![Angular](https://img.shields.io/badge/Frontend-Angular%2018-dd0031?logo=angular)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python)

---

## 🌟 Key Features

- 📚 **Multi-Criteria Sorting**: Sort books by:
  - **Author**: Smart natural sorting by author's last name primary, full name secondary.
  - **Title**: Case-insensitive title sort ignoring leading articles ("The", "A", "An").
  - **Publisher**: Publisher name string sorting.
  - **ISBN Number**: Normalizes ISBN-10 & ISBN-13 (stripping non-digits) for digit-by-digit comparison.
- 🔍 **Instant Search & Filter**: Real-time filtering across titles, authors, publishers, and ISBN numbers.
- ➕ **Add & Delete Books**: Modal form with client and server-side validation.
- 🔄 **Reset Dataset**: One-click restore to the default rich sample dataset.
- 🎨 **Modern Responsive Design**: Styled with a clean design system, status badges, and interactive column indicators (▲ / ▼).

---

## 📁 Repository Structure

```
book-sorter-app/
├── backend/            # FastAPI Python backend
│   ├── main.py         # REST API routes & CORS configuration
│   ├── models.py       # Pydantic schemas for Book models & sorting
│   ├── services.py     # Sorting logic & sample data store
│   ├── test_main.py    # Pytest automated unit tests
│   └── requirements.txt
└── frontend/           # Angular frontend SPA
    ├── src/
    │   ├── app/
    │   │   ├── models/book.model.ts
    │   │   ├── services/book.service.ts
    │   │   └── components/
    │   │       ├── book-list/
    │   │       └── book-form/
    └── angular.json
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Node.js**: v18+ or v22+
- **Python**: 3.10+

### 2. Launch Backend (FastAPI)
```bash
cd backend
python3 -m pip install -r requirements.txt
python3 -m uvicorn main:app --reload --port 8000
```
- API Swagger Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Launch Frontend (Angular)
```bash
cd frontend
npm install
npx ng serve --port 4200
```
- Open application in browser: [http://localhost:4200](http://localhost:4200)

---

## 🧪 Running Unit Tests

To run the backend pytest test suite:
```bash
cd backend
python3 -m pytest -v test_main.py
```
