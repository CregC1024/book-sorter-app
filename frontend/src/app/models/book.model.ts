export type SortField = 'title' | 'author' | 'publisher' | 'isbn';
export type SortOrder = 'asc' | 'desc';

export interface Book {
  id: number;
  title: string;
  author: string;
  publisher: string;
  isbn: string;
  clean_isbn: string;
}

export interface BookCreate {
  title: string;
  author: string;
  publisher: string;
  isbn: string;
}

export interface BookListResponse {
  books: Book[];
  total: number;
  sort_by: SortField;
  sort_order: SortOrder;
  search_query?: string;
}
