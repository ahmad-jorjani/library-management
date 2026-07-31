from pydantic import BaseModel, EmailStr, PositiveInt, Field, field_validator


class MemberCreate(BaseModel):
    """Model used when creating a new member."""

    name: str = Field(min_length=3, max_length=60)
    phone: str | None = Field(default=None, pattern=r"^09\d{9}$")
    email: EmailStr

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        return value.strip().title()


class Member(MemberCreate):
    id: PositiveInt

    def __str__(self):
        phone = self.phone if self.phone is not None else "N/A"

        return f"[{self.id}] {self.name:<20} | {self.email:<25} | {phone:>10}"
