from pydantic import ValidationError
from models.member import MemberCreate
from library import Library
from exceptions import *


def member_menu(library: Library):
    while True:
        show_member_menu()
        choice = input("Enter Your Choice: ")

        try:
            match choice:
                case "1":
                    add_member_ui(library)

                case "2":
                    find_member_ui(library)

                case "3":
                    show_members_ui(library)

                case "4":
                    remove_member_ui(library)

                case "5":
                    update_member_ui(library)

                case "0":
                    print("Thank You for visiting Member Menu!")
                    break

                case _:
                    print("Invalid Choice!")

        except LibraryError as e:
            print(e)

        except ValidationError as e:
            print(e)


def show_member_menu():
    menu = """
============== Member ==============
1. Add Member
2. Find Member
3. Show Members
4. Remove Member
5. Update Member
0. Exit
        """
    print(menu)


def add_member_ui(library: Library):
    name = input("enter your member name: ")
    phone = input("enter your phone: ")
    email = input("enter your email: ")

    if not phone:
        phone = None

    member_data = MemberCreate(name=name, phone=phone, email=email)
    member_id = library.add_member(member_data)
    member = library.find_member(member_id)
    print(member)


def find_member_ui(library: Library):
    try:
        member_id = int(input("enter member id: "))

    except ValueError:
        print("Member id must be positive integer!")

    else:
        member = library.find_member(member_id)
        print(member)


def show_members_ui(library: Library):
    members = library.show_members()

    for member in members:
        print(member)


def remove_member_ui(library: Library):
    try:
        member_id = int(input("enter member id: "))

    except ValueError:
        print("Member id must be positive integer!")

    else:
        removed = library.remove_member(member_id)
        if removed:
            print("Member Deleted...")


def update_member_ui(library: Library):
    update_fields = {"1": "name", "2": "phone", "3": "email"}

    try:
        member_id = int(input("enter member id: "))

    except ValueError:
        print("Member id must be positive integer!")

    else:
        member = library.find_member(member_id)
        print(member)
        print("""
which field do you want to change?
1. Name
2. Phone
3. Email
0. Exit
            """)

        while True:
            choice_update = input("enter your choice to update: ")

            if choice_update == "0":
                break

            if choice_update not in update_fields:
                print("Invalid Choice Chose 0 to 3")
                continue

            field = update_fields[choice_update]
            value = input("enter new value to update: ")

            if not value:
                value = None

            update_member = library.update_member_field(member, field, value)
            print(update_member)
            break
