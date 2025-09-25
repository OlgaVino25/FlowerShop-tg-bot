from datetime import datetime


CURRENT_DATE = datetime.now().strftime('%Y-%m-%d')
CURRENT_TIME = datetime.now().time()


def validate_name(name):
    if not isinstance(name, str) or len(name.strip()) == 0:
        return False, 'Имя обязательно для заполнения'
    return True, ''


def validate_phone(phone):
    phone = ''.join(filter(str.isdigit, phone))
    if len(phone) != 11 or not phone.startswith('7'):
        return False, 'Телефон должен содержать 11 цифр и начинаться с цифры 7'
    return True, ''


def validate_address(address):
    if not isinstance(address, str) or len(address.strip()) == 0:
        return False, 'Адрес обязателен для заполнения'
    return True, ''


def validate_delivery_date_and_time(date_str, time_str):

    try:

        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        time_obj = datetime.strptime(time_str, "%H:%M").time()

        current_date = datetime.strptime(CURRENT_DATE, "%Y-%m-%d").date()
        current_time = CURRENT_TIME

        if time_obj < datetime.strptime("10:00", "%H:%M").time() or \
           time_obj >= datetime.strptime("22:00", "%H:%M").time():
            return False, 'Доставка доступна только с 10:00 до 22:00.'

        if date_obj == current_date and current_time >= datetime.strptime("18:00", "%H:%M").time():
            return False, 'Заказ оформлен после 18:00, доставка возможна только на следующий день.'

        if date_obj < current_date:
            return False, 'Выбранная дата уже прошла.'

        return True, None
    except ValueError:
        return False, 'Неправильно указаны дата или время доставки.'


def main():
    name = input("Ваше имя: ")
    phone = input("Телефон: ")
    address = input("Адрес доставки: ")
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
        delivery_date, delivery_time)
    if not is_valid_delivery_date_and_time:
        errors.append(message)

    if errors:
        for err in errors:
            print(err)
    else:
        print("Данные введены корректно.")


if __name__ == '__main__':
    main()
