from telebot import types
from demo_data.demo_db import add_consultation, find_user
from tg_bot.keyboards import create_phone_keyboard
from tg_bot.filters import contact_filter
import demo_data.demo_db as db


def handle_consultation_contact(bot, message, user_data):
    user_id = message.chat.id
    phone = message.contact.phone_number
    
    consultation_data = add_consultation(
        customer=user_id,
        phone=phone,
        occasion=getattr(user_data[user_id], "occasion", "не указан"),
        budget=0,
        preferred_colors=[user_data[user_id].color_scheme] if user_data[user_id].color_scheme else [],
        excluded_flowers=user_data[user_id].excluded_flowers,
    )

    # Уведомление флористу (заглушка)
    florist_chat_id = 000000000  # Заменить на реальный ID флориста
    try:
        bot.send_message(
            florist_chat_id,
            f"📞 *Новая консультация!*\n\n"
            f"Клиент: {message.chat.first_name}\n"
            f"Телефон: {phone}\n"
            f"Повод: {getattr(user_data[user_id], 'occasion', 'не указан')}\n"
            f"ID консультации: {consultation_data['pk']}",
            parse_mode="Markdown",
        )
    except:
        pass

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("💐 Посмотреть букеты"))

    bot.send_message(
        message.chat.id,
        "✅ *Консультация заказана!*\n\n"
        "Флорист скоро свяжется с вами. А пока можете присмотреть что-нибудь из готовой коллекции!",
        reply_markup=markup,
        parse_mode="Markdown",
    )

    user_data[user_id].consultation_mode = False

def setup_consultation_handlers(bot, user_data):
    
    @bot.callback_query_handler(func=lambda call: call.data == "consultation")
    def handle_consultation_callback(call):
        markup = create_phone_keyboard()
        bot.send_message(
            call.message.chat.id,
            "👩‍🎨 *Заказ консультации флориста*\n\n"
            "Укажите номер телефона, и наш флорист перезвонит вам в течение 20 минут!",
            reply_markup=markup,
            parse_mode="Markdown",
        )
        user_data[call.message.chat.id].consultation_mode = True
        bot.answer_callback_query(call.id)

    @bot.message_handler(func=lambda message: contact_filter(message) and 
                      user_data.get(message.chat.id) and 
                      getattr(user_data[message.chat.id], "consultation_mode", False))
    def consultation_contact_handler(message):
        handle_consultation_contact(bot, message, user_data)