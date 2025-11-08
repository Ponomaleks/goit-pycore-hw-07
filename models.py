from collections import UserDict
from datetime import datetime, timedelta
import re
from typing import Generic, TypeVar, TypedDict

from error_handlers import ValidationError

T = TypeVar("T")


class BirthdayInfo(TypedDict):
    name: str
    congratulation_date: str


class Field(Generic[T]):

    def __init__(self, value: T) -> None:
        self.__value = value

    def __str__(self) -> str:
        return str(self.__value)

    @property
    def value(self) -> T:
        return self.__value

    @value.setter
    def value(self, new_value: T) -> None:
        self.__value = new_value


class Name(Field):
    # реалізація класу
    pass


class Phone(Field[str]):
    def __init__(self, value) -> None:
        if not re.fullmatch(r"\d{10}", value):
            raise ValidationError("The number must consist of 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def __str__(self) -> str:
        if not self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        self.phones = list(filter(lambda el: el.value != phone, self.phones))

    def find_phones(self) -> list[Phone]:
        return self.phones

    def find_phone(self, phone: str) -> Phone | None:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def edit_phone(self, record: str, new_phone: str) -> None:
        phone = self.find_phone(record)
        if phone:
            phone.value = new_phone
        else:
            raise ValueError("Phone number not found.")

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)


class Birthday(Field[datetime]):
    date_format = "%d.%m.%Y"

    def __init__(self, value: str) -> None:
        try:
            date_obj = datetime.strptime(value, Birthday.date_format)
            super().__init__(date_obj)

        except ValueError:
            raise ValidationError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        return self.value.strftime(Birthday.date_format)


class AddressBook(UserDict[str, "Record"]):
    def __str__(self) -> str:
        return "\n".join(f"{key}: {value}" for key, value in self.data.items())

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Contact not found.")

    def get_upcoming_birthdays(self) -> list[BirthdayInfo]:
        upcoming = []
        today = datetime.now().date()
        current_year = today.year

        for name, record in self.data.items():
            if record.birthday:
                date_format = record.birthday.date_format
                birthday_date = record.birthday.value.date()
                birthday_this_year = birthday_date.replace(year=current_year)

                next_birthday = (
                    birthday_this_year
                    if birthday_this_year > today
                    else birthday_date.replace(year=current_year + 1)
                )

                days_before_birthday = (next_birthday - today).days

                if days_before_birthday > 6:
                    continue

                week_day = next_birthday.weekday()
                if week_day >= 5:
                    next_birthday += timedelta(days=7 - week_day)

                upcoming.append(
                    {
                        "name": name,
                        "congratulation_date": next_birthday.strftime(date_format),
                    }
                )
        return upcoming
