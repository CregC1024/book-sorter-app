import { Injectable, signal, computed, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Book, BookCreate, BookListResponse, SortField, SortOrder } from '../models/book.model';
import { catchError, of, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BookService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api/books';

  // Reactive State Signals
  readonly books = signal<Book[]>([]);
  readonly loading = signal<boolean>(false);
  readonly error = signal<string | null>(null);

  readonly sortBy = signal<SortField>('title');
  readonly sortOrder = signal<SortOrder>('asc');
  readonly searchQuery = signal<string>('');

  // Computed local sort signal (supports instantaneous offline/client sorting as well)
  readonly sortedBooks = computed(() => {
    const rawBooks = this.books();
    const query = this.searchQuery().toLowerCase().trim();
    const field = this.sortBy();
    const order = this.sortOrder();

    let list = [...rawBooks];

    // Filter
    if (query) {
      list = list.filter(b =>
        b.title.toLowerCase().includes(query) ||
        b.author.toLowerCase().includes(query) ||
        b.publisher.toLowerCase().includes(query) ||
        b.isbn.toLowerCase().includes(query)
      );
    }

    // Sort
    list.sort((a, b) => {
      let valA = '';
      let valB = '';

      if (field === 'title') {
        valA = a.title.replace(/^(the|a|an)\s+/i, '').toLowerCase();
        valB = b.title.replace(/^(the|a|an)\s+/i, '').toLowerCase();
      } else if (field === 'author') {
        const getLastName = (authorStr: string) => {
          const firstAuthor = authorStr.split(',')[0].trim();
          const parts = firstAuthor.split(' ');
          return parts[parts.length - 1].toLowerCase();
        };
        valA = getLastName(a.author);
        valB = getLastName(b.author);
      } else if (field === 'publisher') {
        valA = a.publisher.toLowerCase();
        valB = b.publisher.toLowerCase();
      } else if (field === 'isbn') {
        valA = a.clean_isbn;
        valB = b.clean_isbn;
      }

      let cmp = valA.localeCompare(valB, undefined, { numeric: true, sensitivity: 'base' });
      return order === 'asc' ? cmp : -cmp;
    });

    return list;
  });

  constructor() {
    this.fetchBooks();
  }

  fetchBooks() {
    this.loading.set(true);
    this.error.set(null);

    let params = new HttpParams()
      .set('sort_by', this.sortBy())
      .set('sort_order', this.sortOrder());

    if (this.searchQuery().trim()) {
      params = params.set('q', this.searchQuery().trim());
    }

    this.http.get<BookListResponse>(this.apiUrl, { params }).pipe(
      tap(res => {
        this.books.set(res.books);
        this.loading.set(false);
      }),
      catchError(err => {
        console.error('Error loading books from API:', err);
        this.error.set('Failed to connect to backend server. Make sure FastAPI server is running on http://localhost:8000.');
        this.loading.set(false);
        return of(null);
      })
    ).subscribe();
  }

  toggleSort(field: SortField) {
    if (this.sortBy() === field) {
      this.sortOrder.update(current => current === 'asc' ? 'desc' : 'asc');
    } else {
      this.sortBy.set(field);
      this.sortOrder.set('asc');
    }
    this.fetchBooks();
  }

  setSearch(query: string) {
    this.searchQuery.set(query);
    this.fetchBooks();
  }

  addBook(book: BookCreate) {
    this.loading.set(true);
    return this.http.post<Book>(this.apiUrl, book).pipe(
      tap(() => {
        this.fetchBooks();
      }),
      catchError(err => {
        console.error('Error adding book:', err);
        this.error.set('Failed to add book.');
        this.loading.set(false);
        return of(null);
      })
    );
  }

  deleteBook(id: number) {
    this.loading.set(true);
    return this.http.delete(`${this.apiUrl}/${id}`).pipe(
      tap(() => {
        this.fetchBooks();
      }),
      catchError(err => {
        console.error('Error deleting book:', err);
        this.error.set('Failed to delete book.');
        this.loading.set(false);
        return of(null);
      })
    );
  }

  resetData() {
    this.loading.set(true);
    return this.http.post<{ message: string }>(`${this.apiUrl}/reset`, {}).pipe(
      tap(() => {
        this.fetchBooks();
      }),
      catchError(err => {
        console.error('Error resetting books:', err);
        this.error.set('Failed to reset dataset.');
        this.loading.set(false);
        return of(null);
      })
    );
  }
}
