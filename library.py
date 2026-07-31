from datetime import date, timedelta

from models.book import BookCreate, Book
from models.member import MemberCreate, Member
from models.borrow import BorrowCreate
from exceptions import *
from database import Database


class Library:
    def __init__(self):
        self.db = Database()
        self.db.create_tables()

    def close(self):
        self.db.close()

    # ? Book
    def add_book(self, book_data: BookCreate) -> int:
        book_id = self.db.add_book(book_data)

        return book_id

    def find_book(self, book_id: int) -> Book:
        book = self.db.get_book_by_id(book_id)

        if book is None:
            raise BookNotFoundError("Book not found!")

        return book

    def show_books(self) -> list[Book]:
        books = self.db.get_all_books()

        # books -> []
        if not books:
            raise BookNotFoundError("No book record!")

        return books

    def remove_book(self, book_id: int):
        removed = self.db.remove_book(book_id)

        if not removed:
            raise BookNotFoundError("Book id is not correct!")

        return True

    def update_book(self, book: Book):
        updated = self.db.update_book(book)

        if not updated:
            raise DatabaseError("Failed to update book!")

        return True

    def update_book_field(self, book: Book, field: str, value: str):
        data = book.model_dump()
        data[field] = value
        updated_book = Book.model_validate(data)
        self.update_book(updated_book)

        return updated_book

    # ? Member
    def add_member(self, member_data: MemberCreate) -> int:
        member_id = self.db.add_member(member_data)

        return member_id

    def find_member(self, member_id: int) -> Member:
        member = self.db.get_member_by_id(member_id)

        if member is None:
            raise MemberNotFoudError("Member not found!")

        return member

    def show_members(self) -> list[Member]:
        members = self.db.get_all_members()

        if not members:
            raise MemberNotFoudError("No member record!")

        return members

    def remove_member(self, member_id: int):
        removed = self.db.remove_member(member_id)

        if not removed:
            raise MemberNotFoudError("Member ID is not correct!")

        return True

    def update_member(self, member: Member):
        updated = self.db.update_member(member)

        if not updated:
            raise Database("Failed to updated member!")

        return True

    def update_member_field(self, member: Member, field: str, value: str) -> Member:
        data = member.model_dump()
        data[field] = value
        updated_member = Member.model_validate(data)
        self.update_member(updated_member)

        return updated_member

    # ? Borrow
    def borrow_book(self, book_id: int, member_id: int) -> int:
        borrow_at = date.today()
        due_at = borrow_at + timedelta(days=14)

        member = self.db.get_member_by_id(member_id)
        book = self.db.get_book_by_id(book_id)

        if member is None:
            raise MemberNotFoudError("Member not found!")

        if book is None:
            raise BookNotFoundError("Book not found!")

        if not book.available:
            raise BookAvailableError("Book is not Available!")

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
            raise BorrowNotFoundError("Borrow not found!")

        if borrow.return_at is not None:
            raise BorrowAlreadyReturnedError(
                f"Book {borrow.book_id} was already returend!"
            )

        borrow.return_at = date.today()
        try:
            result = self.db.update_return_date(borrow.id, borrow.return_at)

            book_result = self.db.set_book_availability(
                book_id=borrow.book_id, available=True
            )

            if not book_result:
                raise DatabaseError("Borrow references missing a book!")

            self.db.commit()

            return result

        except Exception:
            self.db.rollback()
            raise

    # ? Borrow View
    def show_borrow_views(self):
        borrow_views = self.db.get_all_borrow_views()

        if not borrow_views:
            raise BorrowNotFoundError("No borrow records found.")

        return borrow_views

    def show_active_borrow_views(self):
        act_borrow_views = self.db.get_active_borrow_views()

        if not act_borrow_views:
            raise BorrowNotFoundError("No active borrows found.")

        return act_borrow_views

    def show_returned_borrow_views(self):
        returned_borrow_views = self.db.get_returned_borrow_views()

        if not returned_borrow_views:
            raise BorrowNotFoundError("No returned borrows found.")

        return returned_borrow_views

    def show_member_history(self, member_id: int):
        member = self.db.get_member_by_id(member_id)

        if member is None:
            raise MemberNotFoudError("Member ID is not correct!")

        member_history = self.db.get_member_borrow_views(member_id)
        if not member_history:
            raise NoBorrowHistoryError("This member has no borrow history.")

        return member_history

    def show_book_history(self, book_id: int):
        book = self.db.get_book_by_id(book_id)

        if book is None:
            raise BookNotFoundError("Book ID is not correct!")

        book_history = self.db.get_book_borrow_views(book_id)

        if not book_history:
            raise NoBorrowHistoryError("This book has no borrow history.")

        return book_history

    def show_overdue_borrow_views(self):
        overdue_borrow_views = self.db.get_overdue_borrow_views()

        if not overdue_borrow_views:
            raise BorrowNotFoundError("No overdue borrows found.")

        return overdue_borrow_views

    def find_borrow_view(self, borrow_id: int):
        borrow_view = self.db.get_borrow_view_by_id(borrow_id)

        if borrow_view is None:
            raise BorrowNotFoundError("Borrow is not found.")

        return borrow_view
