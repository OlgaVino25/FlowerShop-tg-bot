from telebot import types
from demo_data.demo_db import find_user, add_user, get_occasions
from tg_bot.keyboards import create_occasion_keyboard
from tg_bot.states import UserState

def send_welcome(bot, message, user_data):
    user_id = message.chat.id
    user_data[user_id] = UserState()

    user = find_user(user_id)
    if not user:
        user_info = bot.get_chat(user_id)
        full_name = user_info.first_name
        if user_info.last_name:
            full_name += " " + user_info.last_name
        add_user(tg_id=user_id, full_name=full_name, address="", phone="")

    markup = create_occasion_keyboard()

    bot.send_message(
        message.chat.id,
        "🌸 *FlowerShop* - букеты со смыслом!\n\n"
        "Вы можете посмотреть всю коллекцию букетов или выбрать подходящий повод, либо укажите свой:",
        reply_markup=markup,
        parse_mode="Markdown",
    )

def handle_other_occasion(bot, message, user_data):
    user_id = message.chat.id
    if user_id not in user_data:
        user_data[user_id] = UserState()

    user_data[user_id].occasion = "другой повод"
    markup = types.ReplyKeyboardRemove()
    bot.send_message(
        message.chat.id,
        "✍️ *Напишите, какой повод:*",
        reply_markup=markup,
        parse_mode="Markdown",
    )
    user_data[user_id].waiting_custom_occasion = True

def handle_custom_occasion(bot, message, user_data):
    user_id = message.chat.id
    custom_occasion = message.text.strip()
    user_data[user_id].waiting_custom_occasion = False
    user_data[user_id].custom_occasion = custom_occasion
    user_data[user_id].occasion = "другой повод"

    from tg_bot.keyboards import create_budget_keyboard
    markup = create_budget_keyboard()

    bot.send_message(
        message.chat.id,
        "💵 *На какую сумму рассчитываете?*",
        reply_markup=markup,
        parse_mode="Markdown",
    )

def setup_start_handlers(bot, user_data):
    @bot.message_handler(commands=["start"])
    def start_handler(message):
        send_welcome(bot, message, user_data)

    @bot.message_handler(func=lambda message: message.text == "другой повод")
    def other_occasion_handler(message):
        handle_other_occasion(bot, message, user_data)