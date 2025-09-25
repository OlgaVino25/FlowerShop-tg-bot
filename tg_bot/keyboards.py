from telebot import types
from demo_data.demo_db import get_occasions, get_color_schemes, get_flowers
import demo_data.demo_db as db

def create_occasion_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    occasions = get_occasions()
    for occasion in occasions:
        markup.add(types.KeyboardButton(occasion.title))
    return markup

def create_budget_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    budgets = ["~500", "~1000", "~2000", "больше", "не важно"]
    for budget in budgets:
        markup.add(types.KeyboardButton(budget))
    return markup

def create_color_scheme_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    color_schemes = get_color_schemes()
    for scheme in color_schemes:
        markup.add(types.KeyboardButton(scheme.title))
    markup.add(types.KeyboardButton("не важно"))
    return markup

def create_flowers_exclusion_keyboard(excluded_flowers):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    flowers = get_flowers()
    flower_buttons = []

    for flower in flowers:
        if flower.pk in excluded_flowers:
            flower_buttons.append(types.KeyboardButton(f"✅ {flower.title}"))
        else:
            flower_buttons.append(types.KeyboardButton(f"❌ {flower.title}"))

    for i in range(0, len(flower_buttons), 2):
        if i + 1 < len(flower_buttons):
            markup.row(flower_buttons[i], flower_buttons[i + 1])
        else:
            markup.row(flower_buttons[i])

    markup.row(types.KeyboardButton("✅ Завершить выбор"))
    return markup

def create_phone_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📱 Отправить мой номер", request_contact=True))
    markup.add(types.KeyboardButton("↩️ Назад к выбору"))
    return markup

def create_date_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Сегодня"), types.KeyboardButton("Завтра"))
    markup.add(types.KeyboardButton("↩️ Назад"))
    return markup

def create_time_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    times = ["10:00-12:00", "12:00-14:00", "14:00-16:00", 
             "16:00-18:00", "18:00-20:00", "20:00-22:00"]
    for i in range(0, len(times), 2):
        if i + 1 < len(times):
            markup.row(types.KeyboardButton(times[i]), types.KeyboardButton(times[i + 1]))
        else:
            markup.row(types.KeyboardButton(times[i]))
    markup.row(types.KeyboardButton("↩️ Назад"))
    return markup

def create_comment_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("✅ Без комментария"))
    markup.add(types.KeyboardButton("↩️ Назад"))
    return markup

def create_bouquet_navigation(bouquet_index, bouquets_count, bouquet_pk):
    markup = types.InlineKeyboardMarkup()
    
    if bouquets_count > 1:
        prev_index = bouquet_index - 1 if bouquet_index > 0 else bouquets_count - 1
        next_index = bouquet_index + 1 if bouquet_index < bouquets_count - 1 else 0

        markup.row(
            types.InlineKeyboardButton("⬅️ Назад", callback_data=f"bouquet_{prev_index}"),
            types.InlineKeyboardButton("Дальше ➡️", callback_data=f"bouquet_{next_index}"),
        )

    markup.row(
        types.InlineKeyboardButton("💐 Заказать этот букет", callback_data=f"order_{bouquet_pk}")
    )

    markup.row(
        types.InlineKeyboardButton("📞 Заказать консультацию", callback_data="consultation"),
        types.InlineKeyboardButton("🌺 Посмотреть всю коллекцию", callback_data="all_collection"),
    )
    return markup