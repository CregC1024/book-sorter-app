import { Component, EventEmitter, Output, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BookCreate } from '../../models/book.model';
import { BookService } from '../../services/book.service';

@Component({
  selector: 'app-book-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './book-form.component.html',
  styleUrls: ['./book-form.component.css']
})
export class BookFormComponent {
  private bookService = inject(BookService);

  @Output() closeModal = new EventEmitter<void>();

  title = '';
  author = '';
  publisher = '';
  isbn = '';
  errorMessage = '';

  onSubmit() {
    if (!this.title.trim() || !this.author.trim() || !this.publisher.trim() || !this.isbn.trim()) {
      this.errorMessage = 'All fields are required.';
      return;
    }

    const cleanIsbn = this.isbn.replace(/[^0-9X]/gi, '');
    if (cleanIsbn.length < 9) {
      this.errorMessage = 'Please enter a valid ISBN-10 or ISBN-13 (at least 9 digits).';
      return;
    }

    const newBook: BookCreate = {
      title: this.title.trim(),
      author: this.author.trim(),
      publisher: this.publisher.trim(),
      isbn: this.isbn.trim()
    };

    this.bookService.addBook(newBook).subscribe(res => {
      if (res) {
        this.closeModal.emit();
      }
    });
  }
}
