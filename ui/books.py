from pydantic import ValidationError
from library import Library
from models.book import BookCreate
from exceptions import *


def book_menu(library: Library):
    while True:
        show_book_menu()

        choice = input("Enter Your Choice: ")
        try:
            match choice:
                case "1":
                    add_book_ui(library)

                case "2":
                    find_book_ui(library)

                case "3":
                    show_books_ui(library)

                case "4":
                    remove_book_ui(library)

                case "5":
                    updated_book_ui(library)

                case "0":
                    print("Thank You for visiting Book Menu!")
                    break

                case _:
                    print("Invalid Choice!")

        except LibraryError as e:
            print(e)

        except ValidationError as e:
            print(e)


def show_book_menu():
    menu_book = """
============== Book ==============
1. Add Book
2. Find Book
3. Show Books
4. Remove Book
5. Update Book
0. Exit
    """
    print(menu_book)


def add_book_ui(library: Library):
    try:
        title = input("enter book title: ")
        author = input("enter book author: ")
        publication_year = input("enter book publication year (for example: 2012): ")
        pages = input("enter book pages: ")

        book_data = BookCreate(
            title=title,
            author=author,
            publication_year=publication_year,
            pages=pages,
        )

    except ValidationError as e:
        print(f"Validation Error: {e}")

    except ValueError as e:
        print(e)

    else:
        book_id = library.add_book(book_data)
        book = library.find_book(book_id)
        print(book)


def find_book_ui(library: Library):
    try:
        book_id = int(input("enter book id: "))
        book = library.find_book(book_id)

    except ValueError:
        print("Book id msut be positive integer!")

    else:
        print(book)


def show_books_ui(library: Library):
    books = library.show_books()

    for book in books:
        print(book)


def remove_book_ui(library: Library):
    try:
        book_id = int(input("enter book id you want to delete: "))

    except ValueError:
        print("Book id msut be positive integer!")

    else:
        removed = library.remove_book(book_id)
        if removed:
            print("Book Deleted...")


def updated_book_ui(library: Library):
    update_fields = {"1": "title", "2": "author", "3": "publication_year", "4": "pages"}

    try:
        book_id = int(input("enter book id you want to update: "))

    except ValueError:
        print("book id must be positive integer!")

    else:
        book = library.find_book(book_id)
        print(book)
        print("""
Which field do you want to change?
1. Title
2. Author
3. Publication year
4. Pages
0. Exit
            """)

        while True:

            choice_update = input("Which one?: ").strip()

            if choice_update == "0":
                break

            if choice_update not in update_fields:
                print("Invalid Choice Chose 0 to 4")
                continue

            field = update_fields[choice_update]
            value = input("enter new value you want: ")

            updated_book = library.update_book_field(book, field, value)
            print(updated_book)
            break
