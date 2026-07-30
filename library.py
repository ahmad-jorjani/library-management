from models.borrow import BorrowCreate
from database import Database
from datetime import date, timedelta


class Library:
    def __init__(self):
        self.db = Database()

    def close(self):
        self.db.close()

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
