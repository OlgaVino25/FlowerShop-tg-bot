import sys
import os
from telebot import types
from pathlib import Path

current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from demo_data.demo_db import get_bouquets, get_flower, get_flowers
from tg_bot.keyboards import create_bouquet_navigation
from tg_bot.states import UserState
from tg_bot.filters import (
    occasion_filter,
    budget_filter,
    color_scheme_filter,
    flower_exclusion_filter,
    finish_flowers_filter,
)


def show_bouquet(bot, message, index, user_data):
    user_id = message.chat.id
    bouquets = user_data[user_id].filtered_bouquets

    if index >= len(bouquets):
        index = 0

    bouquet = bouquets[index]
    user_data[user_id].current_bouquet_index = index

    flowers_info = []
    for flower_id in bouquet.flowers:
        flower = get_flower(flower_id)
        if flower:
            flowers_info.append(flower.title)

    markup = create_bouquet_navigation(index, len(bouquets), bouquet.pk)

    caption = f"""
*{bouquet.title}* 💐

*Смысл:* {bouquet.meaning}

*Состав:* {', '.join(flowers_info)}
*Цветовая гамма:* {bouquet.color_scheme}
*Цена:* {bouquet.price} руб.

*Повод:* {bouquet.occasion}
    """

    try:
        if bouquet.image.startswith(("http://", "https://")):
            bot.send_photo(
                message.chat.id,
                bouquet.image,
                caption=caption,
                reply_markup=markup,
                parse_mode="Markdown",
            )
        else:
            with open(bouquet.image, "rb") as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption=caption,
                    reply_markup=markup,
                    parse_mode="Markdown",
                )
    except Exception as e:
        bot.send_message(
            message.chat.id, caption, reply_markup=markup, parse_mode="Markdown"
        )


def show_filtered_bouquets(bot, message, user_data):
    user_id = message.chat.id
    if user_id not in user_data:
        from tg_bot.start import send_welcome
        send_welcome(bot, message, user_data)
        return

    all_bouquets = get_bouquets()
    filtered = []

    # Безопасно получаем атрибуты с значениями по умолчанию
    occasion = getattr(user_data[user_id], "occasion", "не важно")
    budget = getattr(user_data[user_id], "budget", "не важно")
    color_scheme = getattr(user_data[user_id], "color_scheme", None)
    excluded_flowers = getattr(user_data[user_id], "excluded_flowers", [])

    for bouquet in all_bouquets:
        matches = True

        # Фильтр по поводу
        if occasion not in ["не важно", "другой повод"]:
            if bouquet.occasion != occasion:
                matches = False

        # Фильтр по бюджету (исправлено)
        if matches and budget != "не важно":
            if budget == "больше":
                if bouquet.price <= 2000:
                    matches = False
            else:
                budget_ranges = {
                    "~500": (0, 500),
                    "~1000": (501, 1000),
                    "~2000": (1001, 2000),
                }
                if budget in budget_ranges:
                    min_price, max_price = budget_ranges[budget]
                    if not (min_price <= bouquet.price <= max_price):
                        matches = False

        # Фильтр по цветовой гамме
        if (
            matches
            and color_scheme
            and color_scheme.lower() not in ["любая"]
        ):
            if bouquet.color_scheme != color_scheme:
                matches = False

        # Фильтр по исключенным цветам
        if matches and excluded_flowers:
            if any(flower in excluded_flowers for flower in bouquet.flowers):
                matches = False

        if matches:
            filtered.append(bouquet)

    user_data[user_id].filtered_bouquets = filtered
    user_data[user_id].current_bouquet_index = 0

    if not filtered:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("💐 Посмотреть всю коллекцию"))
        markup.add(types.KeyboardButton("📞 Заказать консультацию"))

        bot.send_message(
            message.chat.id,
            "😔 *К сожалению, по вашим критериям не найдено подходящих букетов.*",
            reply_markup=markup,
            parse_mode="Markdown",
        )
        return

    markup = types.ReplyKeyboardRemove()
    bot.send_message(
        message.chat.id,
        "🔍 *Подбираю подходящие букеты...*",
        reply_markup=markup,
        parse_mode="Markdown",
    )
    show_bouquet(bot, message, 0, user_data)


def setup_bouquet_handlers(bot, user_data):

    @bot.message_handler(
        func=lambda message: message.text == "💐 Показать всю коллекцию"
    )
    def handle_show_all_collection(message):
        user_id = message.chat.id
        if user_id not in user_data:
            user_data[user_id] = UserState()

        # Фильтры для показа всей коллекции
        user_data[user_id].occasion = "не важно"
        user_data[user_id].budget = "не важно"
        user_data[user_id].color_scheme = None
        user_data[user_id].color_scheme_set = False
        user_data[user_id].excluded_flowers = []

        all_bouquets = get_bouquets()
        user_data[user_id].filtered_bouquets = all_bouquets
        user_data[user_id].current_bouquet_index = 0

        if not all_bouquets:
            bot.send_message(
                message.chat.id,
                "😔 *В коллекции пока нет букетов.*",
                parse_mode="Markdown",
            )
            return

        markup = types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            "🌸 *Показываю всю коллекцию букетов...*",
            reply_markup=markup,
            parse_mode="Markdown",
        )
        show_bouquet(bot, message, 0, user_data)

    @bot.message_handler(func=lambda message: occasion_filter(message))
    def handle_occasion(message):
        user_id = message.chat.id
        if user_id not in user_data:
            user_data[user_id] = UserState()

        user_data[user_id].occasion = message.text
        # Сбрасываем предыдущие выборы для нового поиска
        user_data[user_id].budget = None
        user_data[user_id].color_scheme = None
        user_data[user_id].color_scheme_set = False
        user_data[user_id].excluded_flowers = []

        from tg_bot.keyboards import create_color_scheme_keyboard

        markup = create_color_scheme_keyboard()

        bot.send_message(
            message.chat.id,
            "🎨 *Выберите цветовую гамму:*",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    # Обработчик цветовой схемы
    @bot.message_handler(func=lambda message: color_scheme_filter(message))
    def handle_color_scheme(message):
        user_id = message.chat.id
        if user_id not in user_data:
            from tg_bot.start import send_welcome

            send_welcome(bot, message, user_data)
            return

        # Проверяем, что цветовая гамма еще не установлена
        if (
            hasattr(user_data[user_id], "color_scheme_set")
            and user_data[user_id].color_scheme_set
        ):
            return

        print(f"Обработка цветовой схемы: {message.text}")

        # Устанавливаем цветовую схему и флаг завершения
        user_data[user_id].color_scheme = message.text
        user_data[user_id].color_scheme_set = True

        # Если выбрано "не важно", сбрасываем цветовую схему
        if message.text.lower() in ["любая"]:
            user_data[user_id].color_scheme = None

        # Убедимся, что excluded_flowers инициализирован
        if (
            not hasattr(user_data[user_id], "excluded_flowers")
            or user_data[user_id].excluded_flowers is None
        ):
            user_data[user_id].excluded_flowers = []

        # Переходим к исключению цветов
        from tg_bot.keyboards import create_flowers_exclusion_keyboard

        markup = create_flowers_exclusion_keyboard(user_data[user_id].excluded_flowers)
        bot.send_message(
            message.chat.id,
            "❌ *Выберите цветы, которые НЕ хотите видеть в букете:*\n\n"
            "Нажмите на цветок, чтобы исключить его из поиска. "
            "Нажмите еще раз, чтобы вернуть.\n\n"
            "Нажмите *✅ Завершить выбор*, когда закончите.",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    @bot.message_handler(func=lambda message: flower_exclusion_filter(message))
    def handle_flower_exclusion(message):
        user_id = message.chat.id
        if user_id not in user_data:
            from tg_bot.start import send_welcome

            send_welcome(bot, message, user_data)
            return

        flower_name = message.text[2:]  # Убираем эмодзи
        flowers = get_flowers()

        flower_found = False
        for flower in flowers:
            if flower.title == flower_name:
                flower_found = True
                if message.text.startswith("❌"):
                    # Исключаем цветок
                    if flower.pk not in user_data[user_id].excluded_flowers:
                        user_data[user_id].excluded_flowers.append(flower.pk)
                        status_msg = f"❌ {flower_name} исключен из поиска"
                else:
                    # Возвращаем цветок
                    if flower.pk in user_data[user_id].excluded_flowers:
                        user_data[user_id].excluded_flowers.remove(flower.pk)
                        status_msg = f"✅ {flower_name} возвращен в поиск"
                break

        if not flower_found:
            return

        # Обновляем клавиатуру
        from tg_bot.keyboards import create_flowers_exclusion_keyboard

        markup = create_flowers_exclusion_keyboard(user_data[user_id].excluded_flowers)

        # Отправляем только статус изменения и обновляем клавиатуру
        bot.send_message(
            message.chat.id,
            status_msg,
            reply_markup=markup,
        )

    @bot.message_handler(func=lambda message: finish_flowers_filter(message))
    def handle_finish_flowers(message):
        user_id = message.chat.id
        if user_id not in user_data:
            from tg_bot.start import send_welcome
            send_welcome(bot, message, user_data)
            return

        from tg_bot.keyboards import create_budget_keyboard

        markup = create_budget_keyboard()

        bot.send_message(
            message.chat.id,
            "💵 *На какую сумму рассчитываете?*",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    # ОБРАБОТЧИК БЮДЖЕТА - ДОЛЖЕН БЫТЬ ПОСЛЕ ВСЕХ ОСТАЛЬНЫХ ОБРАБОТЧИКОВ
    @bot.message_handler(func=lambda message: budget_filter(message))
    def handle_budget(message):
        user_id = message.chat.id
        if user_id not in user_data:
            from tg_bot.start import send_welcome
            send_welcome(bot, message, user_data)
            return

        # Устанавливаем бюджет
        user_data[user_id].budget = message.text
        print(f"Установлен бюджет: {user_data[user_id].budget}")

        # Если выбран "не важно", сразу показываем букеты
        if message.text.lower() in ["не важно"]:
            user_data[user_id].budget = "не важно"
            show_filtered_bouquets(bot, message, user_data)
            return

        # Показываем отфильтрованные букеты
        show_filtered_bouquets(bot, message, user_data)

    @bot.message_handler(func=lambda message: message.text == "💐 Посмотреть букеты")
    def show_bouquets_again(message):
        user_id = message.chat.id
        if user_id in user_data and user_data[user_id].filtered_bouquets:
            show_bouquet(
                bot, message, user_data[user_id].current_bouquet_index, user_data
            )
        else:
            from tg_bot.start import send_welcome

            send_welcome(bot, message, user_data)

    @bot.message_handler(
        func=lambda message: message.text == "💐 Посмотреть всю коллекцию"
    )
    def show_all_collection(message):
        user_id = message.chat.id
        if user_id not in user_data:
            user_data[user_id] = UserState()

        user_data[user_id].occasion = "не важно"
        user_data[user_id].budget = "не важно"
        user_data[user_id].color_scheme = None
        user_data[user_id].excluded_flowers = []

        all_bouquets = get_bouquets()
        user_data[user_id].filtered_bouquets = all_bouquets
        user_data[user_id].current_bouquet_index = 0

        if not all_bouquets:
            bot.send_message(
                message.chat.id,
                "😔 *В коллекции пока нет букетов.*",
                parse_mode="Markdown",
            )
            return

        markup = types.ReplyKeyboardRemove()
        bot.send_message(
            message.chat.id,
            "🌸 *Показываю всю коллекцию букетов...*",
            reply_markup=markup,
            parse_mode="Markdown",
        )
        show_bouquet(bot, message, 0, user_data)