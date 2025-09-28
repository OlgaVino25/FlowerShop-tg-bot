import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from demo_data.demo_db import get_occasions, get_color_schemes, get_flowers
import demo_data.demo_db as db


def occasion_filter(message):
    occasions = [occ.title for occ in get_occasions()]
    return message.text in occasions or message.text == "другой повод"


def budget_filter(message):
    budgets = ["~500", "~1000", "~2000", "больше", "не важно"]
    budgets_lower = [b.lower() for b in budgets]
    result = message.text.lower() in budgets_lower
    return result


def color_scheme_filter(message):
    schemes = [scheme.title for scheme in get_color_schemes()]
    schemes.append("любая")
    return message.text in schemes


def flower_exclusion_filter(message):
    flowers = [flower.title for flower in get_flowers()]
    return (message.text.startswith("❌ ") or message.text.startswith("✅ ")) and any(
        flower in message.text for flower in flowers
    )


def finish_flowers_filter(message):
    return message.text == "✅ Завершить выбор"


def contact_filter(message):
    return message.content_type == "contact"


# Фильтры для заказов
def address_filter(message, user_data):
    user_id = message.chat.id
    return (
        user_id in user_data
        and hasattr(user_data[user_id], "phone")
        and not hasattr(user_data[user_id], "order_address")
    )


def date_filter(message, user_data):
    user_id = message.chat.id
    return (
        user_id in user_data
        and hasattr(user_data[user_id], "order_address")
        and not hasattr(user_data[user_id], "delivery_date")
    )


def time_filter(message, user_data):
    user_id = message.chat.id
    return (
        user_id in user_data
        and hasattr(user_data[user_id], "delivery_date")
        and not hasattr(user_data[user_id], "delivery_time")
    )


def comment_filter(message, user_data):
    user_id = message.chat.id
    return (
        user_id in user_data
        and hasattr(user_data[user_id], "delivery_time")
        and not hasattr(user_data[user_id], "comment")
    )
