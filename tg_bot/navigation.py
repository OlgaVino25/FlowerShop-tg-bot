from telebot import types
from tg_bot.states import UserState
from tg_bot.keyboards import (
    create_phone_keyboard,
    create_date_keyboard,
    create_time_keyboard,
    create_comment_keyboard,
)


def setup_navigation_handlers(bot, user_data):

    @bot.callback_query_handler(func=lambda call: call.data.startswith("bouquet_"))
    def handle_bouquet_navigation(call):
        user_id = call.message.chat.id
        if user_id not in user_data:
            from tg_bot.start import send_welcome
            send_welcome(bot, call.message, user_data)
            return

        index = int(call.data.split("_")[1])
        from tg_bot.bouquets import show_bouquet
        show_bouquet(bot, call.message, index, user_data)
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda call: call.data == "all_collection")
    def handle_all_collection(call):
        user_id = call.message.chat.id
        if user_id not in user_data:
            user_data[user_id] = UserState()

        user_data[user_id].occasion = "не важно"
        user_data[user_id].budget = "не важно"
        user_data[user_id].color_scheme = None
        user_data[user_id].excluded_flowers = []

        from demo_data.demo_db import get_bouquets
        user_data[user_id].filtered_bouquets = get_bouquets()
        user_data[user_id].current_bouquet_index = 0

        if user_data[user_id].filtered_bouquets:
            from tg_bot.bouquets import show_bouquet
            show_bouquet(bot, call.message, 0, user_data)
        else:
            bot.send_message(
                call.message.chat.id,
                "😔 *В коллекции пока нет букетов.*",
                parse_mode="Markdown",
            )
        bot.answer_callback_query(call.id)

    @bot.message_handler(func=lambda message: message.text == "↩️ Назад к выбору")
    def back_to_selection(message):
        user_id = message.chat.id
        if user_id not in user_data:
            from tg_bot.start import send_welcome
            send_welcome(bot, message, user_data)
            return

        # Полная очистка состояния
        user_data[user_id] = UserState()

        from tg_bot.start import send_welcome
        send_welcome(bot, message, user_data)

    @bot.message_handler(func=lambda message: message.text == "↩️ Назад")
    def handle_main_back(message):
        user_id = message.chat.id
        if user_id not in user_data:
            from tg_bot.start import send_welcome
            send_welcome(bot, message, user_data)
            return

        # Если есть активный заказ, откатываем состояние
        if hasattr(user_data[user_id], 'order_state'):
            current_state = user_data[user_id].order_state
            
            if current_state == 'phone':
                user_data[user_id].order_state = 'name'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(types.KeyboardButton("↩️ Назад к выбору"))
                bot.send_message(
                    message.chat.id,
                    "👤 *Как вас зовут?*",
                    reply_markup=markup,
                    parse_mode="Markdown",
                )
            elif current_state == 'address':
                user_data[user_id].order_state = 'phone'
                markup = create_phone_keyboard()
                bot.send_message(
                    message.chat.id,
                    "📞 *Для оформления заказа нам нужен ваш номер телефона:*",
                    reply_markup=markup,
                    parse_mode="Markdown",
                )
            # Добавьте другие состояния по необходимости
        else:
            from tg_bot.start import send_welcome
            send_welcome(bot, message, user_data)