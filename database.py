import sqlite3
from sqlite3 import Row
from datetime import date
from models.book import BookCreate, Book
from models.member import MemberCreate, Member
from models.borrow import Borrow, BorrowView


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

    def _rows_to_borrows(self, rows: list[Row]) -> list[Borrow]:
        return [self._row_to_borrow(row) for row in rows]

    def _row_to_borrow_view(self, row: Row) -> BorrowView:
        return BorrowView(
            borrow_id=row["borrow_id"],
            book_id=row["book_id"],
            book_title=row["book_title"],
            member_id=row["member_id"],
            member_name=row["member_name"],
            borrow_at=row["borrow_at"],
            due_date=row["due_date"],
            return_at=row["return_at"],
        )

    def _rows_to_borrow_views(self, rows: list[Row]) -> list[BorrowView]:
        return [self._row_to_borrow_view(row) for row in rows]

    def _borrow_view_query(
        self, where_sql: str = "", params: tuple = ()
    ) -> list[BorrowView]:

        query = """
            SELECT
                borrows.id AS borrow_id,
                books.id AS book_id,
                books.title AS book_title,
                members.id AS member_id,
                members.name AS member_name,
                
                borrows.borrow_at,
                borrows.due_date,
                borrows.return_at
            FROM borrows
            
            JOIN books
            ON borrows.book_id = books.id
            
            JOIN members
            ON borrows.member_id = members.id
            """

        if where_sql:
            query += "\n" + where_sql

        self.cursor.execute(query, params)

        rows = self.cursor.fetchall()
        return self._rows_to_borrow_views(rows)

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
        self.commit()

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
        self.commit()

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
        self.commit()

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
        self.commit()

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
        self.commit()

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
        self.commit()

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

    # ! Borrow View
    def get_all_borrow_views(self) -> list[BorrowView]:
        return self._borrow_view_query()

    def get_active_borrow_views(self):
        where_sql = "WHERE borrows.return_at IS NULL"

        return self._borrow_view_query(where_sql)

    def get_returned_borrow_views(self):
        where_sql = "WHERE borrows.return_at IS NOT NULL"

        return self._borrow_view_query(where_sql)

    def get_member_borrow_views(self, member_id: int):
        where_sql = "WHERE borrows.member_id = ?"
        params = (member_id,)

        return self._borrow_view_query(where_sql, params)

    def get_book_borrow_views(self, book_id: int):
        where_sql = "WHERE borrows.book_id = ?"
        params = (book_id,)

        return self._borrow_view_query(where_sql, params)

    def get_overdue_borrow_views(self):
        where_sql = "WHERE borrows.return_at IS NULL AND borrows.due_date < ?"
        params = (date.today(),)

        return self._borrow_view_query(where_sql, params)

    def get_borrow_view_by_id(self, borrow_id: int) -> BorrowView | None:
        where_sql = "WHERE borrows.id = ?"
        params = (borrow_id,)

        view = self._borrow_view_query(where_sql, params)
        if not view:
            return None

        return view[0]
