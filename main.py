from library import Library
from ui.books import book_menu
from ui.members import member_menu
from exceptions import *


def show_main_menu():
    menu = """
============== Library ==============
1. Book
2. Member
3. Borrow
0. Exit
"""
    print(menu)


def main():
    library = Library()
    try:
        while True:
            try:
                show_main_menu()
                choice = input("Which Menu do you want to go: ")

                match choice:
                    case "1":
                        book_menu(library)

                    case "2":
                        member_menu(library)

                    case "3":
                        pass

                    case "0":
                        print("Thank You For Using Library System Program, GoodBye!")
                        break

                    case _:
                        print("Invalid Choce!")

            except Exception as e:
                print(f"Unexpected Error: {e}")

    finally:
        library.close()


if __name__ == "__main__":
    main()
