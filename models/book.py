from pydantic import BaseModel, Field, PositiveInt, field_validator, ConfigDict
from datetime import date


class BookCreate(BaseModel):
    """Model used when creating a new book."""

    title: str = Field(min_length=3, max_length=150)
    author: str = Field(min_length=3, max_length=100)
    publication_year: int = Field(ge=1450, le=date.today().year)
    pages: PositiveInt = Field(le=3000)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        return value.strip().title()

    @field_validator("author")
    @classmethod
    def validate_author(cls, value: str):
        return value.strip().title()


class Book(BookCreate):
    id: PositiveInt
    available: bool = True

    def __str__(self):
        status = "Yes" if self.available else "No"

        return (
            f"Book ID: {self.id}\n"
            f"Title: {self.title}\n"
            f"Author: {self.author}\n"
            f"Publication Year: {self.publication_year}\n"
            f"Pages: {self.pages}\n"
            f"Available: {status}"
        )
