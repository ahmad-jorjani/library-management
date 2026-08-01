from pydantic import ValidationError
from library import Library
from models.borrow import BorrowView
from exceptions import LibraryError


def borrow_menu(library: Library):
    while True:
        show_borrow_menu()
        choice = input("enter your choice: ")

        try:
            match choice:
                case "1":
                    borrow_book_ui(library)

                case "2":
                    return_book_ui(library)

                case "3":
                    find_borrow_view_ui(library)

                case "4":
                    show_borrow_views_ui(library)

                case "5":
                    show_active_borrow_views_ui(library)

                case "6":
                    show_returned_borrow_views_ui(library)

                case "7":
                    show_overdue_borrow_views_ui(library)

                case "8":
                    show_member_history_ui(library)

                case "9":
                    show_book_history_ui(library)

                case "0":
                    print("Thank you for visiting Borrow menu!")
                    break

                case _:
                    print("Invalid Choice!")

        except LibraryError as e:
            print(e)

        except ValidationError as e:
            print(e)

        except Exception as e:
            print(e)


def show_borrow_menu():
    menu = """
============== Borrow ==============
1. Borrow Book
2. Return Book
3. Find Borrow
4. Borrows
5. Active Borrows
6. Returned Borrows
7. Overdue Borrows
8. Member History
9. Book History 
0. Exit
        """

    print(menu)


def borrow_book_ui(library: Library):
    try:
        book_id = int(input("enter book id: "))
        member_id = int(input("enter member id: "))

    except ValueError:
        print("IDs must be positive integer!")

    else:
        borrow_id = library.borrow_book(book_id, member_id)
        borrowed_book = library.find_borrow_view(borrow_id)
        print(borrowed_book)


def return_book_ui(library: Library):
    try:
        borrow_id = int(input("enter borrow id you want to return: "))

    except ValueError:
        print("borrow id must be positive integer!")

    else:
        result = library.return_book(borrow_id)
        if result:
            print("Book Returned...")


def find_borrow_view_ui(library: Library):
    try:
        borrow_id = int(input("enter borrow id: "))

    except ValueError:
        print("borrow id must be positive integer!")

    else:
        borrow = library.find_borrow_view(borrow_id)
        print(borrow)


def show_borrow_views_ui(library: Library):
    borrow_list = library.show_borrow_views()
    for borrow in borrow_list:
        print(borrow)


def show_active_borrow_views_ui(library: Library):
    active_borrow_list = library.show_active_borrow_views()
    for borrow in active_borrow_list:
        print(borrow)


def show_returned_borrow_views_ui(library: Library):
    returned_borrow_list = library.show_returned_borrow_views()

    for borrow in returned_borrow_list:
        print(borrow)


def show_overdue_borrow_views_ui(library: Library):
    overdue_borrow_list = library.show_overdue_borrow_views()

    for borrow in overdue_borrow_list:
        print(borrow)


def show_member_history_ui(library: Library):
    try:
        member_id = int(input("enter member id: "))

    except ValueError:
        print("member id must be positive integer!")

    else:
        member_history_list = library.show_member_history(member_id)

        for member_history in member_history_list:
            print(member_history)


def show_book_history_ui(library: Library):
    try:
        book_id = int(input("enter book id: "))

    except ValueError:
        print("book id must be positive integer!")

    else:
        book_history_list = library.show_book_history(book_id)

        for book_history in book_history_list:
            print(book_history)
