from colorama import Fore
from error_handlers import input_error, DataError
from models import AddressBook, Record
from utils import display_contacts


@input_error
def add_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, prev_phone, new_phone = args

    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    else:
        record.edit_phone(prev_phone, new_phone)
        return f"Contact updated from {prev_phone} on {new_phone}."


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    else:
        return f"{name}'s phone numbers: {'; '.join(p.value for p in record.find_phones())}"


@input_error
def show_all(book: AddressBook):
    if not book:
        return "No contacts found."

    print("Contacts list:")
    contacts_table = display_contacts(list(book.values()))
    return contacts_table


@input_error
def delete_contact(args, book: AddressBook):
    name = args[0]
    book.delete(name)
    return "Contact deleted."


@input_error
def show_help():
    print("The list of commands:")
    print(f"{Fore.YELLOW}'Hello'{Fore.RESET} - greet the bot")
    print(f"{Fore.YELLOW}'Add <name> <phone>'{Fore.RESET} - add a contact")
    print(
        f"{Fore.YELLOW}'Сhange <name> <new_phone>'{Fore.RESET} - change a contact's phone number"
    )
    print(f"{Fore.YELLOW}'Phone <name>'{Fore.RESET} - show contact's phone number")
    print(f"{Fore.YELLOW}'Delete <name>'{Fore.RESET} - delete contact")
    print(f"{Fore.YELLOW}'All'{Fore.RESET} - show all contacts")
    print(
        f"{Fore.YELLOW}'Add-birthday <name> <date-of-birth>'{Fore.RESET} - add the contact's birthday"
    )
    print(
        f"{Fore.YELLOW}'Show-birthday <name>'{Fore.RESET} - show the contact's birthday"
    )
    print(f"{Fore.YELLOW}'Birthdays'{Fore.RESET} - show upcoming birthdays")
    print(f"{Fore.YELLOW}'Close' or 'Exit'{Fore.RESET} - exit the program")
    print(f"{Fore.YELLOW}'Help'{Fore.RESET} - show this help message")


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise DataError("Enter user name and birthday.")

    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    else:
        record.add_birthday(birthday)
        return f"Birthday {birthday} added to contact {name}."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    else:
        if record.birthday is None:
            return "Birthday not set for this contact."

        return f"{name}'s birthday is on {record.birthday}."


@input_error
def birthdays(book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays found."

    lines = [
        "Upcoming birthdays:",
        *[f'{info["name"]}: {info["congratulation_date"]}' for info in upcoming],
    ]
    return "\n".join(lines)
