import re
from collections import UserDict

def normalize_phone(number):
    # Видалення всіх символів, які не є цифрами або знаком "+"
    number = re.sub(r"[^\d+]", "", number)

    # Перевірка на різні формати телефонних номерів
    if len(number) == 10 and number.isdigit():
        return '+38' + number  # 10 цифр
    elif len(number) == 11 and number.startswith("+0") and number[2:].isdigit():
        return '+380' + number[2:]  # 10 цифр
    elif len(number) == 10 and number.startswith("+") and number[1:].isdigit():
        return '+380' + number[1:]  # 10 цифр
    elif len(number) == 12 and number.isdigit():
        return "+" + number  # 12 цифр без +
    elif len(number) == 13 and number.startswith("+") and number[1:].isdigit():
        return number  # + та 12 цифр
    elif len(number) == 13 and number.startswith("+38") and number[3:].isdigit() and len(number[3:]) == 10:
        return number  # +38 та 10 цифр
    elif len(number) == 12 and number.startswith("380") and number[3:].isdigit() and len(number[3:]) == 9:
        return "+" + number  # 380 та 9 цифр
    elif len(number) == 11 and number.startswith("0") and number[1:].isdigit():
        return "+38" + number[1:]  # + та 10 цифр, що починаються з 0
    return None


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, *numbers):
        self.numbers = list(numbers)
        self.value = []
        self._normalize_all_phones()

    def _normalize_all_phones(self):
        for number in self.numbers:
            normalized_phone = normalize_phone(number)
            if isinstance(normalized_phone, str):
                self.value.append(normalized_phone)

    def add_phone(self, number):
        normalized_number = normalize_phone(number)
        if isinstance(normalized_number, str):
            self.value.append(normalized_number)

    def find_phone(self, number):
        normalized_phone_number = normalize_phone(number)
        return normalized_phone_number in self.value

    def edit_phone(self, old_number, new_number):
        for index, num in enumerate(self.value):
            if num == normalize_phone(old_number):
                print(f"Змінюємо номер {num} на {normalize_phone(new_number)}.")  # Вивід для відладки
                self.value[index] = normalize_phone(new_number)  # Оновлюємо значення
                return True
        print(f"Номер {old_number} не знайдено.")  # Вивід для відладки
        return False

    def remove_phone(self):
        self.value = []


class Record:
    def __init__(self, name, *phones):
        self.name = Name(name)
        self.phones = []
        self.add_record(*phones)

    def add_record(self, *numbers):
        for number in numbers:
            phone = Phone(number)
            if phone.value:
                self.phones.append(phone)

    def find_record(self, number):
        for phone in self.phones:
            if phone.find_phone(normalize_phone(number)):
                return phone.value
        return None

    def edit_record(self, old_number, new_number):
        for phone in self.phones:
            if phone.find_phone(normalize_phone(old_number)):
                phone.edit_phone(old_number, new_number)
                return True
        return False

    def remove_record(self, number):
        self.phones = [phone for phone in self.phones if not phone.find_phone(normalize_phone(number))]

    def __str__(self):
        phones = ', '.join(p for phone in self.phones for p in phone.value)
        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    def add_address(self, address):
        self.data[address.name.value] = address

    def find_address(self, query):
        # Перевіряємо, чи це ім'я (алфавітні символи) або телефонний номер
        if query.isdigit() or query.startswith("+"):
            normalized_number = normalize_phone(query)  # Нормалізуємо номер для пошуку
            for record in self.data.values():
                for phone in record.phones:
                    if normalized_number in phone.value:
                        return record
        else:
            # Пошук за ім'ям
            return self.data.get(query, None)
        return None

    def edit_address(self, name, new_address):
        self.data[name] = new_address

    def delete_address(self, name):
        if name in self.data:
            del self.data[name]


if __name__ == '__main__':
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_record("1234567890")
    john_record.add_record("5555555555")

    # Додавання запису John до адресної книги
    book.add_address(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_record("9876543210")
    book.add_address(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find_address("John")
    john.edit_record("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_record("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete_address("Jane")
    print(f'Jane has been deleted: {jane_record}')
