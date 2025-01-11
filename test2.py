import re

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
    # Якщо телефонний номер не підходить під жоден з форматів
    return None


print(normalize_phone('+381234567890'))  # Виведе: +381234567890
print(normalize_phone('0523456781'))   # Виведе: 381234567890
print(normalize_phone('1503456782'))
print(normalize_phone('+280503456783'))
print(normalize_phone('+381503456785'))
print(normalize_phone('380503456786'))
print(normalize_phone('+0503456787'))
print(normalize_phone('+503456788'))
