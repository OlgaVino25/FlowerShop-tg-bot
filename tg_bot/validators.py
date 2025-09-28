from datetime import datetime
import re

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().time()


def validate_name(name):
    stripped_name = name.strip()
    if not stripped_name:
        return False, "Имя обязательно для заполнения"

    if len(stripped_name) < 2:
        return False, "Имя должно содержать хотя бы 2 символа"

    if re.search(r"[0-9]", stripped_name):
        return False, "Имя не должно содержать цифры"

    if re.search(r"[^\w\s\-]", stripped_name):
        return False, "Имя содержит недопустимые символы"

    return True, ""


def validate_phone(phone):
    # Если это контакт, номер уже приходит в формате +7...
    # Если ручной ввод, очищаем от лишних символов
    clean_phone = re.sub(r"[^\d+]", "", str(phone))

    # Убираем + если есть
    if clean_phone.startswith("+"):
        clean_phone = clean_phone[1:]

    if len(clean_phone) == 11:
        if clean_phone.startswith("7") or clean_phone.startswith("8"):
            return True, ""
    elif len(clean_phone) == 10:
        # Если ввели без 7 или 8
        return True, ""

    return (
        False,
        "Телефон должен содержать 10-11 цифр. Пример: 9123456789 или +79123456789",
    )


def validate_address(address):
    required_words = ["Красноярск", "улица", "дом"]
    words_in_address = set(word.lower() for word in address.split())

    missing_words = [
        word for word in required_words if word.lower() not in words_in_address
    ]
    if missing_words:
        return (
            False,
            f"В адресе отсутствуют обязательные слова: {' '.join(missing_words)}",
        )
    return True, ""


def validate_delivery_date_and_time(date_str, time_str):

    try:

        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time_str, "%H:%M").time()

        current_date = datetime.strptime(CURRENT_DATE, "%Y-%m-%d").date()
        current_time = CURRENT_TIME

        if (
            time_obj < datetime.strptime("10:00", "%H:%M").time()
            or time_obj >= datetime.strptime("22:00", "%H:%M").time()
        ):
            return False, "Доставка доступна только с 10:00 до 22:00."

        if (
            date_obj == current_date
            and current_time >= datetime.strptime("18:00", "%H:%M").time()
        ):
            return (
                False,
                "Заказ оформлен после 18:00, доставка возможна только на следующий день.",
            )

        if date_obj < current_date:
            return False, "Выбранная дата уже прошла."

        return True, None
    except ValueError:
        return False, "Неправильно указаны дата или время доставки."


def main():
    name = input("Ваше имя: ")
    phone = input("Телефон: ")
    address = input("Адрес доставки (пример: Красноярск, улица. Мира, дом. 10): ")
    delivery_date = input("Дата доставки (ГГГГ-ММ-ДД): ")
    delivery_time = input("Время доставки (ЧЧ:ММ): ")

    errors = []

    is_valid_name, message = validate_name(name)
    if not is_valid_name:
        errors.append(message)

    is_valid_phone, message = validate_phone(phone)
    if not is_valid_phone:
        errors.append(message)

    is_valid_address, message = validate_address(address)
    if not is_valid_address:
        errors.append(message)

    is_valid_delivery_date_and_time, message = validate_delivery_date_and_time(
        delivery_date, delivery_time
    )
    if not is_valid_delivery_date_and_time:
        errors.append(message)

    if errors:
        for err in errors:
            print(err)
    else:
        print("Данные введены корректно.")


if __name__ == "__main__":
    main()
