from telebot import types
from demo_data.demo_db import get_bouquets
from tg_bot.states import UserState
import demo_data.demo_db as db


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

    # Обработчик для кнопки "Показать всю коллекцию"
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
        user_state = user_data.get(user_id)

        if not user_state:
            from tg_bot.start import send_welcome

            send_welcome(bot, message, user_data)
            return

        # Очищаем временные данные заказа
        order_attrs = [
            "consultation_mode",
            "order_bouquet_pk",
            "phone",
            "order_address",
            "delivery_date",
            "delivery_time",
            "comment",
            "order_name",
            "waiting_order_name",
        ]

        for attr in order_attrs:
            if hasattr(user_state, attr):
                delattr(user_state, attr)

        # Возвращаем к выбору букетов
        if hasattr(user_state, "filtered_bouquets") and user_state.filtered_bouquets:
            from tg_bot.bouquets import show_bouquet

            show_bouquet(bot, message, user_state.current_bouquet_index, user_data)
        else:
            from tg_bot.start import send_welcome

            send_welcome(bot, message, user_data)

    @bot.message_handler(func=lambda message: message.text == "↩️ Назад")
    def handle_main_back(message):
        user_id = message.chat.id
        user_state = user_data.get(user_id)

        if not user_state:
            from tg_bot.start import send_welcome

            send_welcome(bot, message, user_data)
            return

        if hasattr(user_state, "filtered_bouquets") and user_state.filtered_bouquets:
            from tg_bot.bouquets import show_bouquet

            show_bouquet(bot, message, user_state.current_bouquet_index, user_data)
        else:
            from tg_bot.start import send_welcome

            send_welcome(bot, message, user_data)
