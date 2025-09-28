import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telebot import types
from datetime import datetime, timedelta
from demo_data.demo_db import add_order, get_bouquet, get_flower
from tg_bot.keyboards import (
    create_phone_keyboard,
    create_date_keyboard,
    create_time_keyboard,
    create_comment_keyboard,
)
from tg_bot.filters import (
    contact_filter,
    address_filter,
    date_filter,
    time_filter,
    comment_filter,
)
from tg_bot.validators import (
    validate_name,
    validate_phone,
    validate_address,
    validate_delivery_date_and_time,
)
import demo_data.demo_db as db


def setup_order_handlers(bot, user_data):

    @bot.callback_query_handler(func=lambda call: call.data.startswith("order_"))
    def handle_order_callback(call):
        user_id = call.message.chat.id
        if user_id not in user_data:
            from tg_bot.start import send_welcome

            send_welcome(bot, call.message, user_data)
            return

        bouquet_pk = int(call.data.split("_")[1])
        user_data[user_id].order_bouquet_pk = bouquet_pk

        # Запрашиваем имя
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("↩️ Назад к выбору"))

        bot.send_message(
            call.message.chat.id,
            "👤 *Как вас зовут?*",
            reply_markup=markup,
            parse_mode="Markdown",
        )
        user_data[user_id].waiting_order_name = True
        bot.answer_callback_query(call.id)

    # Обработчик для имени с валидацией
    @bot.message_handler(
        func=lambda message: user_data.get(message.chat.id)
        and getattr(user_data[message.chat.id], "waiting_order_name", False)
    )
    def handle_order_name(message):
        user_id = message.chat.id

        if message.text == "↩️ Назад к выбору":
            from tg_bot.navigation import back_to_selection

            back_to_selection(message)
            return

        # Валидация имени
        is_valid, error_msg = validate_name(message.text)
        if not is_valid:
            bot.send_message(message.chat.id, f"❌ {error_msg}")
            return

        user_data[user_id].order_name = message.text
        user_data[user_id].waiting_order_name = False
        user_data[user_id].waiting_phone = True

        from tg_bot.keyboards import create_phone_keyboard

        markup = create_phone_keyboard()

        bot.send_message(
            message.chat.id,
            "📞 *Для оформления заказа нам нужен ваш номер телефона:*",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    @bot.message_handler(
        func=lambda message: contact_filter(message)
        and user_data.get(message.chat.id)
        and not getattr(user_data[message.chat.id], "consultation_mode", False)
        and hasattr(user_data[message.chat.id], "order_name")
    )
    def handle_order_contact(message):
        user_id = message.chat.id
        phone = message.contact.phone_number

        # Валидация телефона
        is_valid, error_msg = validate_phone(phone)
        if not is_valid:
            bot.send_message(message.chat.id, f"❌ {error_msg}")
            return

        user_data[user_id].phone = phone
        user_data[user_id].waiting_phone = False  # Добавьте эту строку

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("↩️ Назад"))

        bot.send_message(
            message.chat.id,
            "🏠 *Укажите адрес доставки:*\n\n_Пример: Красноярск, улица Мира, дом 10_",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    @bot.message_handler(func=lambda message: message.text == "📝 Ввести номер вручную")
    def handle_manual_phone_input(message):
        user_id = message.chat.id
        if user_id not in user_data:
            return

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("↩️ Назад к выбору"))

        bot.send_message(
            message.chat.id,
            "📞 *Введите ваш номер телефона:*\n\n_Пример: 9123456789 или +79123456789_",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    @bot.message_handler(func=lambda message: address_filter(message, user_data))
    def handle_address(message):
        print(f"Обработка адреса: {message.text}")
        if message.text == "↩️ Назад":
            markup = create_phone_keyboard()
            bot.send_message(
                message.chat.id,
                "📞 *Для оформления заказа нам нужен ваш номер телефона:*",
                reply_markup=markup,
                parse_mode="Markdown",
            )
            # Удаляем телефон чтобы вернуться к его вводу
            if hasattr(user_data[message.chat.id], "phone"):
                delattr(user_data[message.chat.id], "phone")
            return

        is_valid, error_msg = validate_address(message.text)
        if not is_valid:
            bot.send_message(message.chat.id, f"❌ {error_msg}")
            return

        user_id = message.chat.id
        user_data[user_id].order_address = message.text

        markup = create_date_keyboard()
        bot.send_message(
            message.chat.id,
            "📅 *Выберите дату доставки:*",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    @bot.message_handler(func=lambda message: date_filter(message, user_data))
    def handle_delivery_date(message):
        if message.text == "↩️ Назад":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("↩️ Назад"))
            bot.send_message(
                message.chat.id,
                "🏠 *Укажите адрес доставки:*",
                reply_markup=markup,
                parse_mode="Markdown",
            )
            return

        user_id = message.chat.id

        if message.text == "Сегодня":
            delivery_date = datetime.now().strftime("%Y-%m-%d")
        elif message.text == "Завтра":
            delivery_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            bot.send_message(
                message.chat.id, "❌ Пожалуйста, выберите 'Сегодня' или 'Завтра'"
            )
            return

        now = datetime.now()
        if now.hour >= 18 and message.text == "Сегодня":
            bot.send_message(
                message.chat.id, "❌ *Магазин работает до 18:00*", parse_mode="Markdown"
            )
            return

        user_data[user_id].delivery_date = delivery_date
        markup = create_time_keyboard()
        bot.send_message(
            message.chat.id,
            "⏰ *Выберите время доставки:*",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    @bot.message_handler(func=lambda message: time_filter(message, user_data))
    def handle_delivery_time(message):
        if message.text == "↩️ Назад":
            markup = create_date_keyboard()
            bot.send_message(
                message.chat.id,
                "📅 *Выберите дату доставки:*",
                reply_markup=markup,
                parse_mode="Markdown",
            )
            return

        user_id = message.chat.id
        user_data[user_id].delivery_time = message.text

        is_valid, error_msg = validate_delivery_date_and_time(
            user_data[user_id].delivery_date, message.text.split("-")[0] + ":00"
        )
        if not is_valid:
            bot.send_message(message.chat.id, f"❌ {error_msg}")
            return

        markup = create_comment_keyboard()
        bot.send_message(
            message.chat.id,
            "💬 *Добавьте комментарий к заказу:*",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    @bot.message_handler(func=lambda message: comment_filter(message, user_data))
    def handle_comment(message):
        if message.text == "↩️ Назад":
            markup = create_time_keyboard()
            bot.send_message(
                message.chat.id,
                "⏰ *Выберите время доставки:*",
                reply_markup=markup,
                parse_mode="Markdown",
            )
            return

        user_id = message.chat.id
        user_data[user_id].comment = (
            "" if message.text == "✅ Без комментария" else message.text
        )

        # Получаем информацию о букете для уведомления
        bouquet = get_bouquet(user_data[user_id].order_bouquet_pk)
        flowers_info = []
        for flower_id in bouquet.flowers:
            flower = get_flower(flower_id)
            if flower:
                flowers_info.append(flower.title)

        order_data = add_order(
            customer=user_id,
            bouquet=user_data[user_id].order_bouquet_pk,
            address=user_data[user_id].order_address,
            delivery_date=user_data[user_id].delivery_date,
            delivery_time=user_data[user_id].delivery_time,
            comment=user_data[user_id].comment,
        )

        # Отправляем уведомление курьеру (фиксированный ID)
        courier_chat_id = 666666666  # ID курьера из demo_data
        try:
            order_summary = f"""
            🚀 *Новый заказ!*
            
            *Заказ №:* {order_data['pk']}
            *Имя:* {user_data[user_id].order_name}
            *Телефон:* {user_data[user_id].phone}
            *Адрес:* {user_data[user_id].order_address}
            *Дата доставки:* {user_data[user_id].delivery_date}
            *Время доставки:* {user_data[user_id].delivery_time}
            *Комментарий:* {user_data[user_id].comment}
            
            *Букет:* {bouquet.title}
            *Цена:* {bouquet.price} руб.
            *Состав:* {', '.join(flowers_info)}
            *Повод:* {bouquet.occasion}
            """
            bot.send_message(courier_chat_id, order_summary, parse_mode="Markdown")
        except Exception as e:
            print(f"Ошибка отправки уведомления курьеру: {e}")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("💐 Новый заказ"))

        bot.send_message(
            message.chat.id,
            f"✅ *Заказ оформлен!*\n\n"
            f"Номер заказа: {order_data['pk']}\n"
            f"Букет: {bouquet.title}\n"
            f"Цена: {bouquet.price} руб.\n"
            f"Адрес: {user_data[user_id].order_address}\n"
            f"Дата: {user_data[user_id].delivery_date}\n"
            f"Время: {user_data[user_id].delivery_time}\n\n"
            f"Курьер уже уведомлен о заказе!",
            reply_markup=markup,
            parse_mode="Markdown",
        )

        # Очищаем данные заказа
        order_attrs = [
            "order_bouquet_pk",
            "order_address",
            "delivery_date",
            "delivery_time",
            "comment",
            "order_name",
            "phone",
        ]
        for attr in order_attrs:
            if hasattr(user_data[user_id], attr):
                delattr(user_data[user_id], attr)

    @bot.message_handler(func=lambda message: message.text == "💐 Новый заказ")
    def new_order(message):
        from tg_bot.start import send_welcome

        send_welcome(bot, message, user_data)


def handle_manual_phone_input_message(bot, message, user_data):
    user_id = message.chat.id

    if message.text == "↩️ Назад к выбору":
        from tg_bot.navigation import back_to_selection

        back_to_selection(message)
        return

    print(f"Обработка ручного ввода телефона: {message.text}")

    # Валидация телефона
    is_valid, error_msg = validate_phone(message.text)
    if not is_valid:
        bot.send_message(message.chat.id, f"❌ {error_msg}")
        return

    user_data[user_id].phone = message.text
    user_data[user_id].waiting_phone = False

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("↩️ Назад"))

    bot.send_message(
        message.chat.id,
        "🏠 *Укажите адрес доставки:*\n\n_Пример: Красноярск, улица Мира, дом 10_",
        reply_markup=markup,
        parse_mode="Markdown",
    )
