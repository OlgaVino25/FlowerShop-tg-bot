from demo_data import models
from datetime import datetime
from demo_data.models import (
    Role,
    User,
    Flower,
    ColorScheme,
    Occasion,
    Bouquet,
    Consultation,
    Order,
)
from demo_data.utils import (
    load_from_json,
    find_value_in_dict,
    find_by_field,
    add_to_json,
    delete_from_json,
)
from os import path
from pathlib import Path


BASE_DIR = Path(__file__).parent
JSON_DIRECTORY = BASE_DIR / "json"
USERS = path.join(JSON_DIRECTORY, "users.json")
ROLES = path.join(JSON_DIRECTORY, "roles.json")
FLOWERS = path.join(JSON_DIRECTORY, "flowers.json")
BOUQUETS = path.join(JSON_DIRECTORY, "bouquets.json")
COLOR_SCHEMES = path.join(JSON_DIRECTORY, "color_schemes.json")
OCCASIONS = path.join(JSON_DIRECTORY, "occasions.json")
ORDERS = path.join(JSON_DIRECTORY, "orders.json")
CONSULTATIONS = path.join(JSON_DIRECTORY, "consultations.json")


def parse_user(user: dict) -> User | None:
    """Парсит словарь с данными пользователя в объект User.
    Args:
        user (dict): Словарь с данными пользователя из JSON

    Returns:
        User | None: Объект пользователя или None если роль не найдена
    """
    role = get_role(user.get("role"))
    if not role:
        return None
    return User(
        user.get("pk"),
        user.get("tg_id"),
        user.get("full_name"),
        role,
        user.get("address"),
        user.get("phone"),
    )


def find_user(tg_id: int) -> models.User | None:
    """Находит пользователя по Telegram ID.
    Args:
        tg_id (int): ID пользователя в Telegram

    Returns:
        User | None: Объект пользователя или None если не найден
    """
    user = find_by_field(USERS, "tg_id", tg_id)
    if user:
        return parse_user(user)
    return None

def get_user(pk: int) -> User | None:
    """Получает пользователя по первичному ключу."""
    user = find_value_in_dict(pk, USERS)
    if not user:
        return None
    return parse_user(user)


def get_users() -> list[User]:
    """Получает список всех пользователей.

    Returns:
        list[User]: Список объектов пользователей
    """
    users = load_from_json(USERS)
    return [parse_user(user) for user in users.values()]


def get_role(pk: int) -> Role | None:
    """Получает роль по первичному ключу.

    Args:
        pk (int): Первичный ключ роли

    Returns:
        Role | None: Объект роли или None если не найдена
    """
    role = find_value_in_dict(pk, ROLES)
    if not role:
        return None
    return Role(role.get("pk"), role.get("title"))


def get_flower(pk: int) -> Flower | None:
    """Получает цветок по первичному ключу.

    Args:
        pk (int): Первичный ключ цветка

    Returns:
        Flower | None: Объект цветка или None если не найден
    """
    flower = find_value_in_dict(pk, FLOWERS)
    if not flower:
        return None
    return Flower(
        flower.get("pk"),
        flower.get("title"),
        flower.get("color"),
        flower.get("price"),
    )


def get_flowers() -> list[Flower]:
    """Получает список всех цветков.

    Returns:
        list[Flower]: Список объектов цветков
    """
    flowers = load_from_json(FLOWERS)
    return [get_flower(int(pk)) for pk in flowers.keys()]


def get_color_scheme(pk: int) -> ColorScheme | None:
    """Получает цветовую схему по первичному ключу.

    Args:
        pk (int): Первичный ключ цветовой схемы

    Returns:
        ColorScheme | None: Объект цветовой схемы или None если не найдена
    """
    scheme = find_value_in_dict(pk, COLOR_SCHEMES)
    if not scheme:
        return None
    return ColorScheme(scheme.get("pk"), scheme.get("title"))


def get_color_schemes() -> list[ColorScheme]:
    """Получает список всех цветовых схем.

    Returns:
        list[ColorScheme]: Список объектов цветовых схем
    """
    schemes = load_from_json(COLOR_SCHEMES)
    return [get_color_scheme(int(pk)) for pk in schemes.keys()]


def get_occasion(pk: int) -> Occasion | None:
    """Получает повод по первичному ключу.

    Args:
        pk (int): Первичный ключ повода

    Returns:
        Occasion | None: Объект повода или None если не найден
    """
    occasion = find_value_in_dict(pk, OCCASIONS)
    if not occasion:
        return None
    return Occasion(occasion.get("pk"), occasion.get("title"))


def get_occasions() -> list[Occasion]:
    """Получает список всех поводов.

    Returns:
        list[Occasion]: Список объектов поводов
    """
    occasions = load_from_json(OCCASIONS)
    return [get_occasion(int(pk)) for pk in occasions.keys()]


def get_bouquet(pk: int) -> Bouquet | None:
    """Получает букет по первичному ключу.
    
    Args:
        pk (int): Первичный ключ букета
        
    Returns:
        Bouquet | None: Объект букета или None если не найден
    """
    bouquet = find_value_in_dict(pk, BOUQUETS)
    if not bouquet:
        return None
    return Bouquet(
        bouquet.get("pk"),
        bouquet.get("title"),
        bouquet.get("price"),
        bouquet.get("budget_category"),
        bouquet.get("image"),
        bouquet.get("occasion"),
        bouquet.get("meaning"),
        bouquet.get("flowers"),
        bouquet.get("color_scheme"),
    )


def get_bouquets() -> list[Bouquet]:
    """Получает список всех букетов.
    
    Returns:
        list[Bouquet]: Список объектов букетов
    """
    bouquets = load_from_json(BOUQUETS)
    return [get_bouquet(int(pk)) for pk in bouquets.keys()]


def get_bouquets_by_occasion(occasion: str) -> list[Bouquet]:
    """Получает букеты, подходящие для определенного повода.
    
    Args:
        occasion (str): Название повода
        
    Returns:
        list[Bouquet]: Список букетов, подходящих для указанного повода
    """
    bouquets = get_bouquets()
    return [b for b in bouquets if b.occasion == occasion]


def get_bouquets_by_budget(budget_category: str) -> list[Bouquet]:
    """Получает букеты, подходящие под определенную бюджетную категорию.
    
    Args:
        budget_category (str): Бюджетная категория (~500, ~1000, ~2000, больше)
        
    Returns:
        list[Bouquet]: Список букетов в указанной бюджетной категории
    """
    bouquets = get_bouquets()
    return [b for b in bouquets if b.budget_category == budget_category]


def get_consultation(pk: int) -> Consultation | None:
    """Получает консультацию по первичному ключу.
    
    Args:
        pk (int): Первичный ключ консультации
        
    Returns:
        Consultation | None: Объект консультации или None если не найдена
    """
    consultation = find_value_in_dict(pk, CONSULTATIONS)
    if not consultation:
        return None
    return Consultation(
        consultation.get("pk"),
        consultation.get("customer"),
        consultation.get("phone"),
        consultation.get("occasion"),
        consultation.get("budget"),
        consultation.get("preferred_colors"),
        consultation.get("excluded_flowers"),
        consultation.get("status"),
        consultation.get("created_at"),
    )


def get_consultations() -> list[Consultation]:
    """Получает список всех консультаций.
    
    Returns:
        list[Consultation]: Список объектов консультаций
    """
    consultations = load_from_json(CONSULTATIONS)
    return [get_consultation(int(pk)) for pk in consultations.keys()]


def get_order(pk: int) -> Order | None:
    """Получает заказ по первичному ключу.
    
    Args:
        pk (int): Первичный ключ заказа
        
    Returns:
        Order | None: Объект заказа или None если не найден
    """
    order = find_value_in_dict(pk, ORDERS)
    if not order:
        return None
    return Order(
        order.get("pk"),
        order.get("customer"),
        order.get("bouquet"),
        order.get("address"),
        order.get("delivery_date"),
        order.get("delivery_time"),
        order.get("comment"),
        order.get("status"),
    )


def get_orders() -> list[Order]:
    """Получает список всех заказов.
    
    Returns:
        list[Order]: Список объектов заказов
    """
    orders = load_from_json(ORDERS)
    return [get_order(int(pk)) for pk in orders.keys()]


def add_user(tg_id: int, full_name: str, address: str, phone: str, role_pk: int = 1):
    """Добавляет нового пользователя в базу данных.
    
    Args:
        tg_id (int): ID пользователя в Telegram
        full_name (str): Полное имя пользователя
        address (str): Адрес пользователя
        phone (str): Номер телефона пользователя
        role_pk (int, optional): ID роли пользователя. По умолчанию 1 (customer)
        
    Returns:
        dict: Данные добавленного пользователя
    """
    user_data = {
        "tg_id": tg_id,
        "full_name": full_name,
        "role": role_pk,
        "address": address,
        "phone": phone,
    }
    return add_to_json(USERS, user_data)


def add_consultation(
    customer: int,
    phone: str,
    occasion: str,
    budget: int,
    preferred_colors: list[str],
    excluded_flowers: list[int],
):
    """Добавляет новую консультацию в базу данных.
    
    Args:
        customer (int): ID клиента
        phone (str): Номер телефона для связи
        occasion (str): Повод для букета
        budget (int): Бюджет клиента
        preferred_colors (list[str]): Предпочитаемые цвета
        excluded_flowers (list[int]): Исключаемые цветы (список ID)
        
    Returns:
        dict: Данные добавленной консультации
    """
    consultation_data = {
        "customer": customer,
        "phone": phone,
        "occasion": occasion,
        "budget": budget,
        "preferred_colors": preferred_colors,
        "excluded_flowers": excluded_flowers,
        "status": "новый",
        "created_at": datetime.now().isoformat(),
    }
    return add_to_json(CONSULTATIONS, consultation_data)


def add_order(
    customer: int,
    bouquet: int,
    address: str,
    delivery_date: str,
    delivery_time: str,
    comment: str = "",
):
    """Добавляет новый заказ в базу данных.
    
    Args:
        customer (int): ID клиента
        bouquet (int): ID букета
        address (str): Адрес доставки
        delivery_date (str): Дата доставки в формате YYYY-MM-DD
        delivery_time (str): Время доставки в формате HH:MM
        comment (str, optional): Комментарий к заказу. По умолчанию ""
        
    Returns:
        dict: Данные добавленного заказа
    """
    order_data = {
        "customer": customer,
        "bouquet": bouquet,
        "address": address,
        "delivery_date": delivery_date,
        "delivery_time": delivery_time,
        "comment": comment,
        "status": "новый",
    }
    return add_to_json(ORDERS, order_data)


def update_order_status(order_pk: int, status: str):
    """Обновляет статус заказа.
    
    Args:
        order_pk (int): Первичный ключ заказа
        status (str): Новый статус заказа
        
    Returns:
        bool: True если обновление успешно, False если заказ не найден
    """
    orders = load_from_json(ORDERS)
    if str(order_pk) in orders:
        orders[str(order_pk)]["status"] = status
        from demo_data.utils import save_readable_json

        save_readable_json(orders, ORDERS)
        return True
    return False


def update_consultation_status(consultation_pk: int, status: str):
    """Обновляет статус консультации.
    
    Args:
        consultation_pk (int): Первичный ключ консультации
        status (str): Новый статус консультации
        
    Returns:
        bool: True если обновление успешно, False если консультация не найдена
    """
    consultations = load_from_json(CONSULTATIONS)
    if str(consultation_pk) in consultations:
        consultations[str(consultation_pk)]["status"] = status
        from demo_data.utils import save_readable_json

        save_readable_json(consultations, CONSULTATIONS)
        return True
    return False


