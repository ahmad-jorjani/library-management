from datetime import date, timedelta
from models.book import BookCreate, Book
from models.member import MemberCreate, Member
from models.borrow import BorrowCreate, Borrow
from database import Database


class Library:
    def __init__(self):
        self.db = Database()

    def close(self):
        self.db.close()

    # ? Book
    def add_book(self, book_data: BookCreate) -> int:
        book_id = self.db.add_book(book_data)

        return book_id

    def find_book(self, book_id: int) -> Book:
        book = self.db.get_book_by_id(book_id)

        if book is None:
            raise ValueError("Book not found!")

        return book

    def show_books(self) -> list[Book]:
        books = self.db.get_all_books()

        # books -> []
        if not books:
            raise ValueError("Database is empty for now!")

        return books

    def remove_book(self, book_id: int):
        removed = self.db.remove_book(book_id)

        if not removed:
            raise ValueError("Book id is not correct!")

        return True

    def update_book(self, book: Book):
        updated = self.db.update_book(book)

        if not updated:
            raise ValueError("Book not Updated!")

        return True

    # ? Member
    def add_member(self, member_data: MemberCreate) -> int:
        member_id = self.db.add_member(member_data)

        return member_id

    def find_member(self, member_id: int) -> Member:
        member = self.db.get_member_by_id(member_id)

        if member is None:
            raise ValueError("Member not found!")

        return member

    def show_members(self) -> list[Member]:
        members = self.db.get_all_members()

        if not members:
            raise ValueError("Database is empty for now!")

        return members

    def remove_member(self, member_id: int):
        removed = self.db.remove_member(member_id)

        if not removed:
            raise ValueError("Member ID is not correct!")

        return True

    def update_member(self, member: Member):
        updated = self.db.update_member(member)

        if not updated:
            raise ValueError("Member not updated!")

        return True

    # ? Borrow
    def borrow_book(self, book_id: int, member_id: int) -> int:
        borrow_at = date.today()
        due_at = borrow_at + timedelta(days=14)

        member = self.db.get_member_by_id(member_id)
        book = self.db.get_book_by_id(book_id)

        if member is None:
            raise ValueError("Member not found!")

        if book is None:
            raise ValueError("Book not found!")

        if not book.available:
            raise ValueError("Book is not Available!")

        borrow_data = BorrowCreate(
            book_id=book_id, member_id=member_id, borrow_at=borrow_at, due_date=due_at
        )
        try:
            borrow_id = self.db.add_borrow(borrow_data)

            self.db.set_book_availability(book_id=book_id, available=False)

            self.db.commit()

            return borrow_id

        except Exception:
            self.db.rollback()
            raise

    def return_book(self, borrow_id: int) -> bool:
        borrow = self.db.get_borrow_by_id(borrow_id)

        if borrow is None:
            raise ValueError("Borrow not found!")

        if borrow.return_at is not None:
            raise ValueError(f"Book {borrow.book_id} was already returend!")

        borrow.return_at = date.today()
        try:
            result = self.db.update_return_date(borrow.id, borrow.return_at)

            book_result = self.db.set_book_availability(
                book_id=borrow.book_id, available=True
            )

            if not book_result:
                raise RuntimeError("Borrow references missing a book!")

            self.db.commit()

            return result

        except Exception:
            self.db.rollback()
            raise
