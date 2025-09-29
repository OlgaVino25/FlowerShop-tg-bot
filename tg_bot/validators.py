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
    """Проверяет валидность адреса доставки."""
    address = address.strip()

    # Проверка длины
    if len(address) < 5:
        return False, "Адрес слишком короткий. Укажите, пожалуйста, полный адрес."

    # Проверка наличия цифр (номера дома)
    if not re.search(r"\d", address):
        return False, "Укажите, пожалуйста, номер дома в адресе."

    return True, ""


def validate_delivery_date_and_time(date_str, time_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Извлекаем время начала из интервала
        start_time_str = time_str.split("-")[0] if "-" in time_str else time_str
        
        time_obj = datetime.strptime(start_time_str, "%H:%M").time()

        current_date = datetime.strptime(CURRENT_DATE, "%Y-%m-%d").date()
        current_time = CURRENT_TIME

        # Проверяем, что время доставки в рабочем диапазоне
        if (
            time_obj < datetime.strptime("10:00", "%H:%M").time()
            or time_obj >= datetime.strptime("22:00", "%H:%M").time()
        ):
            return False, "Доставка доступна только с 10:00 до 22:00."

        # Проверяем, что если заказ сегодня, то время должно быть позже текущего
        if date_obj == current_date:
            if time_obj <= current_time:
                return False, "Выбранное время уже прошло. Пожалуйста, выберите более позднее время."
            
            if current_time >= datetime.strptime("18:00", "%H:%M").time():
                return (
                    False,
                    "Заказ оформлен после 18:00, доставка возможна только на следующий день.",
                )

        # Проверяем, что дата не в прошлом
        if date_obj < current_date:
            return False, "Выбранная дата уже прошла."

        return True, None
    except ValueError as e:
        print(f"Ошибка валидации даты/времени: {e}")
        return False, "Неправильно указаны дата или время доставки."
