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
from tg_bot.validators import (
    validate_name,
    validate_phone,
    validate_address,
    validate_delivery_date_and_time,
)


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
        user_data[user_id].order_state = 'name'

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("↩️ Назад к выбору"))

        bot.send_message(
            call.message.chat.id,
            "👤 *Как вас зовут?*",
            reply_markup=markup,
            parse_mode="Markdown",
        )
        bot.answer_callback_query(call.id)

    # Обработчик имени
    @bot.message_handler(func=lambda message: user_data.get(message.chat.id) and 
                      getattr(user_data[message.chat.id], 'order_state', None) == 'name')
    def handle_order_name(message):
        user_id = message.chat.id

        if message.text == "↩️ Назад к выбору":
            from tg_bot.navigation import back_to_selection
            back_to_selection(message)
            user_data[user_id].order_state = None
            return

        is_valid, error_msg = validate_name(message.text)
        if not is_valid:
            bot.send_message(message.chat.id, f"❌ {error_msg}")
            return

        user_data[user_id].order_name = message.text
        user_data[user_id].order_state = 'phone'

        markup = create_phone_keyboard()
        bot.send_message(
            message.chat.id,
            "📞 *Для оформления заказа нам нужен ваш номер телефона:*",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    # Обработчик телефона через контакт
    @bot.message_handler(content_types=['contact'], 
                      func=lambda message: user_data.get(message.chat.id) and 
                      getattr(user_data[message.chat.id], 'order_state', None) == 'phone')
    def handle_order_contact(message):
        user_id = message.chat.id
        phone = message.contact.phone_number

        is_valid, error_msg = validate_phone(phone)
        if not is_valid:
            bot.send_message(message.chat.id, f"❌ {error_msg}")
            return

        user_data[user_id].phone = phone
        user_data[user_id].order_state = 'address'

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("↩️ Назад"))

        bot.send_message(
            message.chat.id,
            "🏠 *Укажите адрес доставки:*\n\n_Пример: Красноярск, улица Мира, дом 10_",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    # Обработчик ручного ввода телефона
    @bot.message_handler(func=lambda message: message.text == "📝 Ввести номер вручную" and
                      user_data.get(message.chat.id) and 
                      getattr(user_data[message.chat.id], 'order_state', None) == 'phone')
    def handle_manual_phone_option(message):
        user_id = message.chat.id

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("↩️ Назад к выбору"))

        bot.send_message(
            message.chat.id,
            "📞 *Введите ваш номер телефона:*\n\n_Пример: 9123456789 или +79123456789_",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    # Обработчик ручного ввода номера
    @bot.message_handler(func=lambda message: user_data.get(message.chat.id) and 
                      getattr(user_data[message.chat.id], 'order_state', None) == 'phone' and
                      message.text not in ["📝 Ввести номер вручную", "↩️ Назад к выбору"])
    def handle_manual_phone_input(message):
        user_id = message.chat.id

        if message.text == "↩️ Назад к выбору":
            from tg_bot.navigation import back_to_selection
            back_to_selection(message)
            user_data[user_id].order_state = None
            return

        is_valid, error_msg = validate_phone(message.text)
        if not is_valid:
            bot.send_message(message.chat.id, f"❌ {error_msg}")
            return

        user_data[user_id].phone = message.text
        user_data[user_id].order_state = 'address'

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("↩️ Назад"))

        bot.send_message(
            message.chat.id,
            "🏠 *Укажите адрес доставки:*\n\n_Пример: Красноярск, улица Мира, дом 10_",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    # Обработчик адреса
    @bot.message_handler(func=lambda message: user_data.get(message.chat.id) and 
                      getattr(user_data[message.chat.id], 'order_state', None) == 'address')
    def handle_address(message):
        user_id = message.chat.id
        
        if message.text == "↩️ Назад":
            user_data[user_id].order_state = 'phone'
            markup = create_phone_keyboard()
            bot.send_message(
                message.chat.id,
                "📞 *Для оформления заказа нам нужен ваш номер телефона:*",
                reply_markup=markup,
                parse_mode="Markdown",
            )
            return

        is_valid, error_msg = validate_address(message.text)
        if not is_valid:
            bot.send_message(message.chat.id, f"❌ {error_msg}")
            return

        user_data[user_id].order_address = message.text
        user_data[user_id].order_state = 'date'

        markup = create_date_keyboard()
        bot.send_message(
            message.chat.id,
            "📅 *Выберите дату доставки:*",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    # Обработчик даты
    @bot.message_handler(func=lambda message: user_data.get(message.chat.id) and 
                      getattr(user_data[message.chat.id], 'order_state', None) == 'date')
    def handle_delivery_date(message):
        user_id = message.chat.id

        if message.text == "↩️ Назад":
            user_data[user_id].order_state = 'address'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("↩️ Назад"))
            bot.send_message(
                message.chat.id,
                "🏠 *Укажите адрес доставки:*",
                reply_markup=markup,
                parse_mode="Markdown",
            )
            return

        now = datetime.now()
        
        # Проверяем время оформления заказа (текущее время)
        if now.hour >= 18:
            # Если после 18:00, доставка только на завтра
            if message.text == "Сегодня":
                bot.send_message(
                    message.chat.id, 
                    "❌ *Заказ оформлен после 18:00, доставка возможна только на следующий день.*", 
                    parse_mode="Markdown"
                )
                return
            elif message.text == "Завтра":
                delivery_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            else:
                bot.send_message(
                    message.chat.id, "❌ Пожалуйста, выберите 'Завтра'"
                )
                return
        else:
            # Если до 18:00, можно выбрать сегодня или завтра
            if message.text == "Сегодня":
                delivery_date = datetime.now().strftime("%Y-%m-%d")
            elif message.text == "Завтра":
                delivery_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            else:
                bot.send_message(
                    message.chat.id, "❌ Пожалуйста, выберите 'Сегодня' или 'Завтра'"
                )
                return

        user_data[user_id].delivery_date = delivery_date
        user_data[user_id].order_state = 'time'

        markup = create_time_keyboard()
        bot.send_message(
            message.chat.id,
            "⏰ *Выберите время доставки:*",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    # Обработчик времени
    @bot.message_handler(func=lambda message: user_data.get(message.chat.id) and 
                      getattr(user_data[message.chat.id], 'order_state', None) == 'time')
    def handle_delivery_time(message):
        user_id = message.chat.id

        if message.text == "↩️ Назад":
            user_data[user_id].order_state = 'date'
            markup = create_date_keyboard()
            bot.send_message(
                message.chat.id,
                "📅 *Выберите дату доставки:*",
                reply_markup=markup,
                parse_mode="Markdown",
            )
            return

        user_data[user_id].delivery_time = message.text

        is_valid, error_msg = validate_delivery_date_and_time(
            user_data[user_id].delivery_date, message.text
        )
        if not is_valid:
            bot.send_message(message.chat.id, f"❌ {error_msg}")
            return

        user_data[user_id].order_state = 'comment'

        markup = create_comment_keyboard()
        bot.send_message(
            message.chat.id,
            "💬 *Добавьте комментарий к заказу:*",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    # Обработчик комментария
    @bot.message_handler(func=lambda message: user_data.get(message.chat.id) and 
                      getattr(user_data[message.chat.id], 'order_state', None) == 'comment')
    def handle_comment(message):
        user_id = message.chat.id

        if message.text == "↩️ Назад":
            user_data[user_id].order_state = 'time'
            markup = create_time_keyboard()
            bot.send_message(
                message.chat.id,
                "⏰ *Выберите время доставки:*",
                reply_markup=markup,
                parse_mode="Markdown",
            )
            return

        # Сохраняем комментарий независимо от выбора
        if message.text == "✅ Без комментария":
            user_data[user_id].comment = ""
        else:
            user_data[user_id].comment = message.text

        print(f"Сохранен комментарий: '{user_data[user_id].comment}'")  # Для отладки

        # Сохраняем заказ
        try:
            order_data = add_order(
                customer=user_id,
                bouquet=user_data[user_id].order_bouquet_pk,
                address=user_data[user_id].order_address,
                delivery_date=user_data[user_id].delivery_date,
                delivery_time=user_data[user_id].delivery_time,
                comment=user_data[user_id].comment,
            )

            # Получаем информацию о букете
            bouquet = get_bouquet(user_data[user_id].order_bouquet_pk)
            flowers_info = []
            for flower_id in bouquet.flowers:
                flower = get_flower(flower_id)
                if flower:
                    flowers_info.append(flower.title)

            # Определяем повод для заказа
            occasion = user_data[user_id].occasion
            if hasattr(user_data[user_id], 'custom_occasion') and user_data[user_id].custom_occasion:
                occasion = user_data[user_id].custom_occasion

            # Формируем сообщение с комментарием
            order_message = f"""✅ *Заказ оформлен!*

Номер заказа: {order_data['pk']}
Повод: {occasion}
Букет: {bouquet.title}
Цена: {bouquet.price} руб.
Имя: {user_data[user_id].order_name}
Телефон: {user_data[user_id].phone}
Адрес: {user_data[user_id].order_address}
Дата: {user_data[user_id].delivery_date}
Время: {user_data[user_id].delivery_time}"""

            # Добавляем комментарий, если он есть
            if user_data[user_id].comment:
                order_message += f"\nКомментарий: {user_data[user_id].comment}"

            order_message += "\n\nКурьер уже уведомлен о заказе!"

            # Уведомление курьеру
            courier_chat_id = 666666666
            try:
                courier_message = f"""🚀 *Новый заказ!*

*Заказ №:* {order_data['pk']}
*Имя:* {user_data[user_id].order_name}
*Телефон:* {user_data[user_id].phone}
*Адрес:* {user_data[user_id].order_address}
*Дата доставки:* {user_data[user_id].delivery_date}
*Время доставки:* {user_data[user_id].delivery_time}
*Повод:* {occasion}"""

                if user_data[user_id].comment:
                    courier_message += f"\n*Комментарий:* {user_data[user_id].comment}"

                courier_message += f"""

*Букет:* {bouquet.title}
*Цена:* {bouquet.price} руб.
*Состав:* {', '.join(flowers_info)}"""

                bot.send_message(courier_chat_id, courier_message, parse_mode="Markdown")
            except Exception as e:
                print(f"Ошибка отправки уведомления курьеру: {e}")

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("💐 Новый заказ"))

            bot.send_message(
                message.chat.id,
                order_message,
                reply_markup=markup,
                parse_mode="Markdown",
            )

        except Exception as e:
            print(f"Ошибка при сохранении заказа: {e}")
            bot.send_message(
                message.chat.id,
                "❌ *Произошла ошибка при оформлении заказа. Попробуйте позже.*",
                parse_mode="Markdown",
            )

        # Очищаем состояние заказа
        user_data[user_id].order_state = None
        for attr in ['order_bouquet_pk', 'order_name', 'phone', 'order_address', 
                    'delivery_date', 'delivery_time', 'comment']:
            if hasattr(user_data[user_id], attr):
                delattr(user_data[user_id], attr)

    @bot.message_handler(func=lambda message: message.text == "💐 Новый заказ")
    def new_order(message):
        from tg_bot.start import send_welcome
        send_welcome(bot, message, user_data)