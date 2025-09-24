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


JSON_DIRECTORY = "demo_data/json/"
USERS = path.join(JSON_DIRECTORY, "users.json")
ROLES = path.join(JSON_DIRECTORY, "roles.json")
FLOWERS = path.join(JSON_DIRECTORY, "flowers.json")
BOUQUETS = path.join(JSON_DIRECTORY, "bouquets.json")
COLOR_SCHEMES = path.join(JSON_DIRECTORY, "color_schemes.json")
OCCASIONS = path.join(JSON_DIRECTORY, "occasions.json")
ORDERS = path.join(JSON_DIRECTORY, "orders.json")
CONSULTATIONS = path.join(JSON_DIRECTORY, "consultations.json")


def parse_user(user: dict) -> User | None:
    """Парсит словарь с данными пользователя в объект User."""
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
    user = find_by_field(USERS, "tg_id", tg_id)
    if user:
        return parse_user(user)
    return None


def get_user(pk: int) -> User | None:
    user = find_value_in_dict(pk, USERS)
    if not user:
        return None
    return parse_user(user)


def get_users() -> list[User]:
    users = load_from_json(USERS)
    return [parse_user(user) for user in users.values()]


def get_role(pk: int) -> Role | None:
    role = find_value_in_dict(pk, ROLES)
    if not role:
        return None
    return Role(role.get("pk"), role.get("title"))


def get_flower(pk: int) -> Flower | None:
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
    flowers = load_from_json(FLOWERS)
    return [get_flower(int(pk)) for pk in flowers.keys()]


def get_color_scheme(pk: int) -> ColorScheme | None:
    scheme = find_value_in_dict(pk, COLOR_SCHEMES)
    if not scheme:
        return None
    return ColorScheme(scheme.get("pk"), scheme.get("title"))


def get_color_schemes() -> list[ColorScheme]:
    schemes = load_from_json(COLOR_SCHEMES)
    return [get_color_scheme(int(pk)) for pk in schemes.keys()]


def get_occasion(pk: int) -> Occasion | None:
    occasion = find_value_in_dict(pk, OCCASIONS)
    if not occasion:
        return None
    return Occasion(occasion.get("pk"), occasion.get("title"))


def get_occasions() -> list[Occasion]:
    occasions = load_from_json(OCCASIONS)
    return [get_occasion(int(pk)) for pk in occasions.keys()]


def get_bouquet(pk: int) -> Bouquet | None:
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
    bouquets = load_from_json(BOUQUETS)
    return [get_bouquet(int(pk)) for pk in bouquets.keys()]


def get_bouquets_by_occasion(occasion: str) -> list[Bouquet]:
    bouquets = get_bouquets()
    return [b for b in bouquets if b.occasion == occasion]


def get_bouquets_by_budget(budget_category: str) -> list[Bouquet]:
    bouquets = get_bouquets()
    return [b for b in bouquets if b.budget_category == budget_category]


def get_consultation(pk: int) -> Consultation | None:
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
    consultations = load_from_json(CONSULTATIONS)
    return [get_consultation(int(pk)) for pk in consultations.keys()]


def get_order(pk: int) -> Order | None:
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
    orders = load_from_json(ORDERS)
    return [get_order(int(pk)) for pk in orders.keys()]


def add_user(tg_id: int, full_name: str, address: str, phone: str, role_pk: int = 1):
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
    orders = load_from_json(ORDERS)
    if str(order_pk) in orders:
        orders[str(order_pk)]["status"] = status
        from demo_data.utils import save_readable_json

        save_readable_json(orders, ORDERS)
        return True
    return False


def update_consultation_status(consultation_pk: int, status: str):
    consultations = load_from_json(CONSULTATIONS)
    if str(consultation_pk) in consultations:
        consultations[str(consultation_pk)]["status"] = status
        from demo_data.utils import save_readable_json

        save_readable_json(consultations, CONSULTATIONS)
        return True
    return False
