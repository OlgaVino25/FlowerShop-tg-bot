from telebot import types
from demo_data.demo_db import add_consultation, find_user
from tg_bot.keyboards import create_phone_keyboard
from tg_bot.filters import contact_filter
from tg_bot.validators import validate_phone
import demo_data.demo_db as db


def handle_consultation_contact(bot, message, user_data):
    user_id = message.chat.id
    phone = message.contact.phone_number

    is_valid, error_msg = validate_phone(phone)
    if not is_valid:
        bot.send_message(message.chat.id, f"❌ {error_msg}")
        return
    
    # Сохраняем консультацию
    consultation_data = add_consultation(
        customer=user_id,
        phone=phone,
        occasion=getattr(user_data[user_id], "occasion", "не указан"),
        budget=0,
        preferred_colors=[user_data[user_id].color_scheme] if user_data[user_id].color_scheme else [],
        excluded_flowers=user_data[user_id].excluded_flowers,
    )

    # Уведомление флористу (замените на реальный ID флориста)
    florist_chat_id = 000000000  # TODO: Заменить на реальный ID флориста
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
    except Exception as e:
        print(f"Ошибка отправки уведомления флористу: {e}")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("💐 Посмотреть букеты"))

    bot.send_message(
        message.chat.id,
        "✅ *Консультация заказана!*\n\n"
        "Флорист свяжется с вами в течение 20 минут. А пока можете присмотреть что-нибудь из готовой коллекции!",
        reply_markup=markup,
        parse_mode="Markdown",
    )

    user_data[user_id].consultation_mode = False


def setup_consultation_handlers(bot, user_data):
    
    @bot.callback_query_handler(func=lambda call: call.data == "consultation")
    def handle_consultation_callback(call):
        user_id = call.message.chat.id
        if user_id not in user_data:
            from tg_bot.start import send_welcome
            send_welcome(bot, call.message, user_data)
            return

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

    @bot.message_handler(func=lambda message: message.text == "📞 Заказать консультацию")
    def handle_consultation_text(message):
        user_id = message.chat.id
        if user_id not in user_data:
            from tg_bot.start import send_welcome
            send_welcome(bot, message, user_data)
            return

        markup = create_phone_keyboard()
        bot.send_message(
            message.chat.id,
            "👩‍🎨 *Заказ консультации флориста*\n\n"
            "Укажите номер телефона, и наш флорист перезвонит вам в течение 20 минут!",
            reply_markup=markup,
            parse_mode="Markdown",
        )
        user_data[user_id].consultation_mode = True

    # Обработчик для контактов в режиме консультации
    @bot.message_handler(content_types=['contact'], 
                      func=lambda message: user_data.get(message.chat.id) and 
                      getattr(user_data[message.chat.id], "consultation_mode", False))
    def consultation_contact_handler(message):
        print("Обработчик контакта для консультации вызван")  # Для отладки
        handle_consultation_contact(bot, message, user_data)

    # Обработчик для ручного ввода номера в режиме консультации
    @bot.message_handler(func=lambda message: 
                      user_data.get(message.chat.id) and 
                      getattr(user_data[message.chat.id], "consultation_mode", False) and
                      message.text not in ["📱 Отправить мой номер", "📝 Ввести номер вручную", "↩️ Назад к выбору"])
    def consultation_manual_phone_handler(message):
        user_id = message.chat.id
        phone = message.text

        # Проверяем валидность номера
        is_valid, error_msg = validate_phone(phone)
        if not is_valid:
            bot.send_message(message.chat.id, f"❌ {error_msg}")
            return
        
        # Сохраняем консультацию
        consultation_data = add_consultation(
            customer=user_id,
            phone=phone,
            occasion=getattr(user_data[user_id], "occasion", "не указан"),
            budget=0,
            preferred_colors=[user_data[user_id].color_scheme] if user_data[user_id].color_scheme else [],
            excluded_flowers=user_data[user_id].excluded_flowers,
        )

        # Уведомление флористу
        florist_chat_id = 000000000  # TODO: Заменить на реальный ID флориста
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
        except Exception as e:
            print(f"Ошибка отправки уведомления флористу: {e}")

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("💐 Посмотреть букеты"))

        bot.send_message(
            message.chat.id,
            "✅ *Консультация заказана!*\n\n"
            "Флорист свяжется с вами в течение 20 минут. А пока можете присмотреть что-нибудь из готовой коллекции!",
            reply_markup=markup,
            parse_mode="Markdown",
        )

        user_data[user_id].consultation_mode = False

    # Обработчик для кнопки "Ввести номер вручную" в режиме консультации
    @bot.message_handler(func=lambda message: 
                      user_data.get(message.chat.id) and 
                      getattr(user_data[message.chat.id], "consultation_mode", False) and
                      message.text == "📝 Ввести номер вручную")
    def handle_manual_phone_option_consultation(message):
        user_id = message.chat.id

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("↩️ Назад к выбору"))

        bot.send_message(
            message.chat.id,
            "📞 *Введите ваш номер телефона:*\n\n_Пример: 9123456789 или +79123456789_",
            reply_markup=markup,
            parse_mode="Markdown",
        )