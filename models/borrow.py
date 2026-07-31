from pydantic import BaseModel, PositiveInt, computed_field
from datetime import date


class BorrowCreate(BaseModel):
    """Model used when creating a new borrow."""

    book_id: PositiveInt
    member_id: PositiveInt
    borrow_at: date
    due_date: date


class Borrow(BorrowCreate):
    id: PositiveInt
    return_at: date | None = None


class BorrowView(BaseModel):
    borrow_id: PositiveInt
    book_id: PositiveInt
    book_title: str
    member_id: PositiveInt
    member_name: str
    borrow_at: date
    due_date: date
    return_at: date | None

    @computed_field
    @property
    def is_late(self) -> bool:
        if self.return_at is None:
            return date.today() > self.due_date

        return self.return_at > self.due_date

    def __str__(self):
        if self.return_at is not None:
            status = "Returned"

        elif self.is_late:
            status = "Overdue"

        else:
            status = "Borrowed"

        return (
            f"Book: {self.book_title}\n"
            f"Member: {self.member_name}\n"
            f"Borrowed: {self.borrow_at}\n"
            f"Due: {self.due_date}\n"
            f"Status: {status}"
        )
