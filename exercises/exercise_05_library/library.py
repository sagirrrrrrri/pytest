"""练习 5：图书馆借阅系统（按 TDD 流程实现我，然后写测试）"""


class Book:
    def __init__(self, isbn: str, title: str, author: str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.available = True  # 是否可借
        self.borrower = None  # 当前借阅人（None 表示无人借）


class Library:
    def __init__(self):
        self.books = {}  # {isbn: Book}

    def add_book(self, isbn: str, title: str, author: str) -> None:
        if isbn in self.books:
            raise ValueError("ISBN 已存在")
        self.books[isbn] = Book(isbn, title, author)

    def borrow(self, isbn: str, user: str) -> None:
        book = self.books.get(isbn)
        if book is None:
            raise KeyError(f"图书不存在: {isbn}")
        if not book.available:
            raise ValueError("图书已被借出")
        book.available = False
        book.borrower = user

    def return_book(self, isbn: str) -> None:
        book = self.books.get(isbn)
        if book is None:
            raise KeyError(f"图书不存在: {isbn}")
        if book.available:
            raise ValueError("图书未被借出")
        book.available = True
        book.borrower = None

    def search_by_title(self, keyword: str) -> list:
        kw = keyword.lower()
        return [book for book in self.books.values() if kw in book.title.lower()]

    def available_books(self) -> list:
        return [book for book in self.books.values() if book.available]

    def borrowed_by(self, user: str) -> list:
        return [book for book in self.books.values() if book.borrower == user]

    @property
    def total_count(self) -> int:
        return len(self.books)
