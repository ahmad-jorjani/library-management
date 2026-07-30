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

    @computed_field
    @property
    def is_late(self) -> bool:
        if self.return_at is None:
            return date.today() > self.due_date

        return self.return_at > self.due_date

    def __str__(self):
        status_returned = "Yes" if self.return_at is not None else "No"
        status_late = "Yes" if not self.is_late else "No"

        return (
            f"Book #{self.book_id} -> Member #{self.member_id}\n"
            f"Borrowed: {self.borrow_at}\n"
            f"Due: {self.due_date}\n"
            f"Returned: {status_returned}\n"
            f"Late: {status_late}"
        )
