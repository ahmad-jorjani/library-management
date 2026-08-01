# Mistakes & Lessons Learned

This file contains mistakes I made while building this project and what I learned from fixing them.

---

## 1. Forgot `WHERE` in UPDATE

### Wrong

```sql
UPDATE books
SET title = ?, author = ?
```

### Correct

```sql
UPDATE books
SET title = ?, author = ?
WHERE id = ?
```

### Lesson

Never write an UPDATE without checking if a WHERE clause is required.

---

## 2. SQL Parameter Order Matters

I accidentally wrote:

```python
(book_id, available)
```

while my SQL query was:

```sql
SET available = ?
WHERE id = ?
```

The correct order is:

```python
(available, book_id)
```

### Lesson

The order of SQL placeholders (`?`) must match the tuple exactly.

---

## 3. Forgot to Call `create_tables()`

I got:

```
no such table: books
```

because I never created the database tables.

### Lesson

Always initialize the database before using it.

---

## 4. `None` Cannot Be Formatted

I wrote:

```python
f"{self.phone:<15}"
```

When phone was `None`, Python raised:

```
unsupported format string passed to NoneType.__format__
```

### Fix

```python
phone = self.phone or "N/A"
```

### Lesson

Always handle optional values before formatting them.

---

## 5. UPDATE Didn't Save

I forgot:

```python
self.commit()
```

### Lesson

Without commit, database changes are not permanently saved.

---

## 6. Transaction for Multi-Step Operations

Borrowing a book requires two database operations:

- Create borrow record
- Mark book as unavailable

If one succeeds and the other fails, the database becomes inconsistent.

### Fix

```python
try:
    ...
    self.db.commit()
except Exception:
    self.db.rollback()
    raise
```

### Lesson

Use transactions whenever multiple database operations must succeed together.

---

## 7. Re-validate Updated Data

Using

```python
setattr(book, field, value)
```

bypasses Pydantic validation.

### Better

```python
data = book.model_dump()
data[field] = value
updated = Book.model_validate(data)
```

### Lesson

Always revalidate data after editing models.

---

## 8. GitHub Didn't Detect Python

GitHub Linguist didn't recognize the repository as Python because there were almost no `.py` files committed yet.

### Lesson

Push the complete project before worrying about GitHub language statistics.

---

## 9. JOIN Is Better for Display

Originally I displayed only IDs:

```
Book ID: 2
Member ID: 5
```

After using JOIN:

```
Book: Clean Code
Member: Ali
```

### Lesson

Database IDs are useful internally, but users should see meaningful information.

---

## 10. SQLite Journal File

I noticed:

```
library.db-journal
```

This is normal.

SQLite creates it during transactions and usually deletes it after a successful commit.

### Lesson

The journal file is part of SQLite's recovery mechanism.

---

## 11. Don't Duplicate Business Logic

Initially I updated book availability by modifying the object directly.

Later I created:

```python
set_book_availability()
```

### Lesson

Keep database update logic inside the database layer.

---

## 12. `raise` vs `raise e`

Inside:

```python
except Exception:
    raise
```

`raise` preserves the original traceback.

### Lesson

Prefer `raise` when rethrowing the same exception.

---

## 13. Custom Exceptions Make UI Cleaner

Instead of:

```python
raise ValueError(...)
```

I created custom exceptions like:

- BookNotFoundError
- MemberNotFoundError
- BorrowNotFoundError

### Lesson

Custom exceptions separate input errors from business logic errors.

---

## 14. Separate UI from Business Logic

Originally everything was inside `main.py`.

Later I created:

```
ui/
    books.py
    members.py
    borrows.py
```

### Lesson

Large CLI projects become much easier to maintain when UI is separated from business logic.

---

## 15. Small Helper Functions Reduce Duplicate SQL

Instead of writing JOIN queries multiple times, I created:

```python
_borrow_view_query(where="", params=())
```

### Lesson

When the SQL is mostly the same, move the common part into a private helper.

---

# Final Thoughts

Building this project taught me:

- Object-Oriented Programming
- SQLite CRUD
- Transactions
- Rollback
- JOIN
- Pydantic Validation
- Layered Architecture
- Exception Handling
- CLI Design
- Clean Code principles

Most importantly:

> Every bug I fixed improved both the project and my understanding of Python.