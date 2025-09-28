import os
import sys
import telebot
from telebot import types
from pathlib import Path
from tg_bot.validators import (
    validate_name,
    validate_phone,
    validate_address,
    validate_delivery_date_and_time,
)
from dotenv import load_dotenv

current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from tg_bot.start import setup_start_handlers
from tg_bot.bouquets import setup_bouquet_handlers
from tg_bot.consultation import setup_consultation_handlers
from tg_bot.order import setup_order_handlers
from tg_bot.navigation import setup_navigation_handlers
from tg_bot.states import UserState

load_dotenv()
token = os.getenv("FLORAL_BOUQUET_BOT_TG_TOKEN")
bot = telebot.TeleBot(token)
user_data = {}


def main():
    setup_start_handlers(bot, user_data)
    setup_consultation_handlers(bot, user_data)
    setup_order_handlers(bot, user_data)
    setup_navigation_handlers(bot, user_data)
    setup_bouquet_handlers(bot, user_data)

    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message):
        user_id = message.chat.id

        if user_id not in user_data:
            from tg_bot.start import send_welcome
            send_welcome(bot, message, user_data)
            return

        # Если есть активный заказ и ждем имя
        if getattr(user_data[user_id], "waiting_order_name", False):
            from tg_bot.order import handle_order_name
            handle_order_name(message)
            return

        # Если есть активный заказ и ждем телефон
        if (getattr(user_data[user_id], "waiting_phone", False) and 
            not getattr(user_data[user_id], "consultation_mode", False)):
            from tg_bot.order import handle_manual_phone_input_message
            handle_manual_phone_input_message(bot, message, user_data)
            return

        print(f"Необработанное сообщение: {message.text}")
        from tg_bot.start import send_welcome
        send_welcome(bot, message, user_data)

    print("Бот запущен...")
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
