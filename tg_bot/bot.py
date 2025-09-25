import os
import sys
import telebot
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

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
    # Регистрация всех обработчиков
    setup_start_handlers(bot, user_data)
    setup_bouquet_handlers(bot, user_data)
    setup_consultation_handlers(bot, user_data)
    setup_order_handlers(bot, user_data)
    setup_navigation_handlers(bot, user_data)

    # Обработчик для кастомного ввода повода
    @bot.message_handler(func=lambda message: user_data.get(message.chat.id) and 
                       getattr(user_data[message.chat.id], "waiting_custom_occasion", False))
    def handle_custom_occasion_fallback(message):
        from tg_bot.start import handle_custom_occasion
        handle_custom_occasion(bot, message, user_data)

    # Обработчик для любых текстовых сообщений (fallback)
    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message):
        user_id = message.chat.id
        
        # Если пользователь не найден, отправляем приветствие
        if user_id not in user_data:
            from tg_bot.start import send_welcome
            send_welcome(bot, message, user_data)
            return
        
        # Если сообщение не обработано другими обработчиками, показываем приветствие
        from tg_bot.start import send_welcome
        send_welcome(bot, message, user_data)

    print("Бот запущен...")
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()