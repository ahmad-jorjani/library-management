import sqlite3
from sqlite3 import Row
from datetime import date
from models.book import BookCreate, Book
from models.member import MemberCreate, Member
from models.borrow import Borrow


class Database:
    def __init__(self, database_name="library.db"):
        self.database_name = database_name

        self.conn = sqlite3.connect(database_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.cursor.execute("PRAGMA foreign_keys = ON")

    # * Book
    def _row_to_book(self, row: Row) -> Book:
        return Book(
            id=row["id"],
            title=row["title"],
            author=row["author"],
            publication_year=row["publication_year"],
            pages=row["pages"],
            available=row["available"],
        )

    def _rows_to_books(self, rows: list[Row]) -> list[Book]:
        return [self._row_to_book(row) for row in rows]

    # * Member
    def _row_to_member(self, row: Row) -> Member:
        return Member(
            id=row["id"], name=row["name"], phone=row["phone"], email=row["email"]
        )

    def _rows_to_members(self, rows: list[Row]) -> list[Member]:
        return [self._row_to_member(row) for row in rows]

    # * Borrow
    def _row_to_borrow(self, row: Row) -> Borrow:
        return Borrow(
            id=row["id"],
            book_id=row["book_id"],
            member_id=row["member_id"],
            borrow_at=row["borrow_at"],
            due_date=row["due_date"],
            return_at=row["return_at"],
        )

    def close(self):
        if self.conn:
            self.conn.close()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    # ! Tables

    def create_books_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publication_year INTEGER NOT NULL,
                pages INTEGER NOT NULL,
                available INTEGER NOT NULL DEFAULT 1
            )
            """)

    def create_members_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT NOT NULL
            )
            """)

    def create_borrows_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                borrow_at TEXT NOT NULL,
                due_date TEXT NOT NULL,
                return_at TEXT,
                FOREIGN KEY (book_id) REFERENCES books(id), 
                FOREIGN KEY (member_id) REFERENCES members(id)
            )
            """)

    def create_tables(self):
        self.create_books_table()
        self.create_members_table()
        self.create_borrows_table()

        self.commit()

    # ! Book CRUD
    def add_book(self, book: BookCreate) -> int:
        self.cursor.execute(
            """
            INSERT INTO books(
                title,
                author,
                publication_year,
                pages
            )
            VALUES(?, ?, ?, ?)
            """,
            (book.title, book.author, book.publication_year, book.pages),
        )

        return self.cursor.lastrowid

    def get_book_by_id(self, book_id) -> Book | None:
        self.cursor.execute(
            """
            SELECT * FROM books WHERE id = ?
            """,
            (book_id,),
        )
        row = self.cursor.fetchone()

        if row is None:
            return None

        return self._row_to_book(row)

    def get_all_books(self) -> list[Book]:
        self.cursor.execute("SELECT * FROM books    ")
        rows = self.cursor.fetchall()

        return self._rows_to_books(rows)

    def remove_book(self, book_id: int) -> bool:
        self.cursor.execute(
            """
            DELETE FROM books WHERE id = ?
            """,
            (book_id,),
        )

        return self.cursor.rowcount > 0

    def update_book(self, book: Book) -> bool:
        self.cursor.execute(
            """
            UPDATE books
            SET title = ?, author = ?, publication_year = ?, pages = ?
            WHERE id = ?
            """,
            (book.title, book.author, book.publication_year, book.pages, book.id),
        )

        return self.cursor.rowcount > 0

    def set_book_availability(self, book_id: int, available: bool) -> bool:
        self.cursor.execute(
            """
            UPDATE books
            SET available = ?
            WHERE id = ?
            """,
            (available, book_id),
        )

        return self.cursor.rowcount > 0

    # ! Member CRUD
    def add_member(self, member: MemberCreate) -> int:
        self.cursor.execute(
            """
            INSERT INTO members(
                name, phone, email
            )
            VALUES (?, ?, ?)
            """,
            (member.name, member.phone, member.email),
        )

        return self.cursor.lastrowid

    def get_member_by_id(self, member_id: int) -> Member | None:
        self.cursor.execute(
            """
            SELECT * FROM members
            WHERE id = ?
            """,
            (member_id,),
        )
        row = self.cursor.fetchone()
        if row is None:
            return None

        return self._row_to_member(row)

    def get_all_members(self) -> list[Member]:
        self.cursor.execute("SELECT * FROM members")
        rows = self.cursor.fetchall()

        return self._rows_to_members(rows)

    def remove_member(self, member_id: int) -> bool:
        self.cursor.execute(
            """
            DELETE FROM members 
            WHERE id = ?
            """,
            (member_id,),
        )

        return self.cursor.rowcount > 0

    def update_member(self, member: Member) -> bool:
        self.cursor.execute(
            """
            UPDATE members
            SET name = ?, phone = ?, email = ?
            WHERE id = ?
            """,
            (member.name, member.phone, member.email, member.id),
        )

        return self.cursor.rowcount > 0

    # ! Borrow
    def add_borrow(self, borrow: Borrow) -> int:
        self.cursor.execute(
            """
            INSERT INTO borrows (
                book_id,
                member_id,
                borrow_at,
                due_at
            )
            VALUES(?,?,?,?)
            """,
            (borrow.book_id, borrow.member_id, borrow.borrow_at, borrow.due_date),
        )

        return self.cursor.lastrowid

    def get_borrow_by_id(self, borrow_id: int) -> Borrow | None:
        self.cursor.execute(
            """
            SELECT * FROM borrows
            WHERE id = ?
            """,
            (borrow_id,),
        )
        row = self.cursor.fetchone()
        if row is None:
            return None

        return self._row_to_borrow(row)

    def update_return_date(self, borrow_id: int, return_at: date) -> bool:
        self.cursor.execute(
            """
            UPDATE borrows
            SET return_at = ?
            WHERE id = ?
            """,
            (borrow_id, return_at),
        )

        return self.cursor.rowcount > 0
