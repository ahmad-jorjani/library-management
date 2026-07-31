class LibraryError(Exception):
    """Base exception for library"""

    pass


class BookNotFoundError(LibraryError):
    pass


class BookAvailableError(LibraryError):
    pass


class MemberNotFoudError(LibraryError):
    pass


class BorrowNotFoundError(LibraryError):
    pass


class BorrowAlreadyReturnedError(LibraryError):
    pass


class NoBorrowHistoryError(LibraryError):
    pass


class DatabaseError(LibraryError):
    pass
