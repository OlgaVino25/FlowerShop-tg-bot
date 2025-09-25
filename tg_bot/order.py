import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telebot import types
from datetime import datetime, timedelta
from demo_data.demo_db import add_order
from tg_bot.keyboards import create_phone_keyboard, create_date_keyboard, create_time_keyboard, create_comment_keyboard
from tg_bot.filters import contact_filter, address_filter, date_filter, time_filter, comment_filter  # Добавлены все фильтры
from tg_bot.validators import validate_address, validate_delivery_date_and_time  # Добавлены валидаторы
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

        markup = create_phone_keyboard()
        bot.send_message(
            call.message.chat.id,
            "📞 *Для оформления заказа нам нужен ваш номер телефона:*",
            reply_markup=markup,
            parse_mode="Markdown",
        )
        bot.answer_callback_query(call.id)

    @bot.message_handler(func=lambda message: contact_filter(message) and 
                      user_data.get(message.chat.id) and 
                      not getattr(user_data[message.chat.id], "consultation_mode", False))
    def handle_order_contact(message):
        user_id = message.chat.id
        phone = message.contact.phone_number
        user_data[user_id].phone = phone

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("↩️ Назад"))

        bot.send_message(
            message.chat.id,
            "🏠 *Укажите адрес доставки:*",
            reply_markup=markup,
            parse_mode="Markdown",
        )

    @bot.message_handler(func=lambda message: address_filter(message, user_data))
    def handle_address(message):
        if message.text == "↩️ Назад":
            from tg_bot.start import send_welcome
            send_welcome(bot, message, user_data)
            return

        is_valid, error_msg = validate_address(message.text)
        if not is_valid:
            bot.send_message(message.chat.id, f"❌ {error_msg}")
            return

        user_id = message.chat.id
        user_data[user_id].order_address = message.text

        markup = create_date_keyboard()
        bot.send_message(message.chat.id, "📅 *Выберите дату доставки:*", 
                        reply_markup=markup, parse_mode="Markdown")

    @bot.message_handler(func=lambda message: date_filter(message, user_data))
    def handle_delivery_date(message):
        if message.text == "↩️ Назад":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("↩️ Назад"))
            bot.send_message(message.chat.id, "🏠 *Укажите адрес доставки:*", 
                           reply_markup=markup, parse_mode="Markdown")
            return

        user_id = message.chat.id

        if message.text == "Сегодня":
            delivery_date = datetime.now().strftime("%Y-%m-%d")
        elif message.text == "Завтра":
            delivery_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            bot.send_message(message.chat.id, "❌ Пожалуйста, выберите 'Сегодня' или 'Завтра'")
            return

        now = datetime.now()
        if now.hour >= 18 and message.text == "Сегодня":
            bot.send_message(message.chat.id, "❌ *Магазин работает до 18:00*", parse_mode="Markdown")
            return

        user_data[user_id].delivery_date = delivery_date
        markup = create_time_keyboard()
        bot.send_message(message.chat.id, "⏰ *Выберите время доставки:*", 
                        reply_markup=markup, parse_mode="Markdown")

    @bot.message_handler(func=lambda message: time_filter(message, user_data))
    def handle_delivery_time(message):
        if message.text == "↩️ Назад":
            markup = create_date_keyboard()
            bot.send_message(message.chat.id, "📅 *Выберите дату доставки:*", 
                           reply_markup=markup, parse_mode="Markdown")
            return

        user_id = message.chat.id
        user_data[user_id].delivery_time = message.text

        is_valid, error_msg = validate_delivery_date_and_time(
            user_data[user_id].delivery_date, 
            message.text.split('-')[0] + ':00'
        )
        if not is_valid:
            bot.send_message(message.chat.id, f"❌ {error_msg}")
            return

        markup = create_comment_keyboard()
        bot.send_message(message.chat.id, "💬 *Добавьте комментарий к заказу:*", 
                        reply_markup=markup, parse_mode="Markdown")

    @bot.message_handler(func=lambda message: comment_filter(message, user_data))
    def handle_comment(message):
        if message.text == "↩️ Назад":
            markup = create_time_keyboard()
            bot.send_message(message.chat.id, "⏰ *Выберите время доставки:*", 
                           reply_markup=markup, parse_mode="Markdown")
            return

        user_id = message.chat.id
        user_data[user_id].comment = "" if message.text == "✅ Без комментария" else message.text

        order_data = add_order(
            customer=user_id,
            bouquet=user_data[user_id].order_bouquet_pk,
            address=user_data[user_id].order_address,
            delivery_date=user_data[user_id].delivery_date,
            delivery_time=user_data[user_id].delivery_time,
            comment=user_data[user_id].comment,
        )

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("💐 Новый заказ"))

        bot.send_message(
            message.chat.id,
            f"✅ *Заказ оформлен!*\n\nНомер заказа: {order_data['pk']}",
            reply_markup=markup,
            parse_mode="Markdown",
        )

        # Очищаем данные заказа
        if hasattr(user_data[user_id], 'order_bouquet_pk'):
            del user_data[user_id].order_bouquet_pk
        if hasattr(user_data[user_id], 'order_address'):
            del user_data[user_id].order_address
        if hasattr(user_data[user_id], 'delivery_date'):
            del user_data[user_id].delivery_date
        if hasattr(user_data[user_id], 'delivery_time'):
            del user_data[user_id].delivery_time
        if hasattr(user_data[user_id], 'comment'):
            del user_data[user_id].comment

    @bot.message_handler(func=lambda message: message.text == "💐 Новый заказ")
    def new_order(message):
        from tg_bot.start import send_welcome
        send_welcome(bot, message, user_data)