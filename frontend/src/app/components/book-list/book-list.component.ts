import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BookService } from '../../services/book.service';
import { SortField } from '../../models/book.model';
import { BookFormComponent } from '../book-form/book-form.component';

@Component({
  selector: 'app-book-list',
  standalone: true,
  imports: [CommonModule, FormsModule, BookFormComponent],
  templateUrl: './book-list.component.html',
  styleUrls: ['./book-list.component.css']
})
export class BookListComponent {
  readonly bookService = inject(BookService);

  showAddModal = signal(false);
  searchInput = signal('');

  onSearchChange(value: string) {
    this.searchInput.set(value);
    this.bookService.setSearch(value);
  }

  onSort(field: SortField) {
    this.bookService.toggleSort(field);
  }

  onDelete(id: number, event: Event) {
    event.stopPropagation();
    if (confirm('Are you sure you want to delete this book?')) {
      this.bookService.deleteBook(id).subscribe();
    }
  }

  onReset() {
    if (confirm('Reset book list back to initial sample dataset?')) {
      this.bookService.resetData().subscribe();
    }
  }
}
