"""Telegram bot."""
# import os
from environs import Env
from telegram import ReplyKeyboardMarkup  # , KeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)


# Этапы разговора
(
    CHOOSING_EVENT,
    TYPING_CUSTOM_EVENT,
    CHOOSING_BUDGET,
    ORDER_OPTIONS,
    CONSULTATION,
    COLLECTION_VIEW
) = range(6)


# Список букетов
BOUQUETS = [
    {
        'photo': 'bouquet.jpg',
        'description': (
            'Букет №1: Нежность... Состав: розы, пионы. Стоимость: 1500 руб.'
        )
    },
    {
        'photo': 'bouquet2.jpeg',
        'description': (
            'Букет №2: Элегантность... Состав: лилии. Стоимость: 2000 руб.'
        )
    }
]
current_bouquet_index = 0  # Индекс текущего букета в коллекции


def start(update, context):
    """Обработчик команды /start."""
    context.user_data.clear()

    event_keyboard = [
        ['День рождения 🎉', 'Свадьба 💒'],
        ['В школу 🎓', 'Без повода 😊'],
        ['Другой повод']
    ]
    reply_markup = ReplyKeyboardMarkup(event_keyboard, resize_keyboard=True)

    update.message.reply_text(
        (
            'К какому событию готовимся?\
            Выберите один из вариантов, либо укажите свой.'
        ),
        reply_markup=reply_markup
    )

    return CHOOSING_EVENT


def event_received(update, context):
    """Обработчик выбора повода."""
    user_choice = update.message.text
    user_data = context.user_data

    if user_choice == 'Другой повод':
        update.message.reply_text('Напишите, какой у вас повод:')
        return TYPING_CUSTOM_EVENT

    user_data['event'] = user_choice

    budget_keyboard = [
        ['~500 руб', '~1000 руб'],
        ['~2000 руб', 'Больше'],
        ['Не важно']
    ]
    reply_markup = ReplyKeyboardMarkup(budget_keyboard, resize_keyboard=True)

    update.message.reply_text(
        'Отлично! На какую сумму рассчитываете?',
        reply_markup=reply_markup
    )
    return CHOOSING_BUDGET


def custom_event_received(update, context):
    """Обработчик ввода своего повода."""
    custom_event = update.message.text
    context.user_data['event'] = f'"{custom_event}"'

    budget_keyboard = [
        ['~500 руб', '~1000 руб'],
        ['~2000 руб', 'Больше'],
        ['Не важно']
    ]
    reply_markup = ReplyKeyboardMarkup(budget_keyboard, resize_keyboard=True)

    update.message.reply_text(
        'Запомнили! На какую сумму рассчитываете?',
        reply_markup=reply_markup
    )
    return CHOOSING_BUDGET


def budget_received(update, context):
    """Обработчик выбора бюджета и показ первого букета."""
    user_budget = update.message.text
    user_event = context.user_data.get('event', 'не указано')

    # Сохраняем бюджет
    context.user_data['budget'] = user_budget

    # Показываем первый букет
    show_bouquet(update, context)

    return ORDER_OPTIONS


def show_bouquet(update, context):
    """Функция показа букета."""
    user_event = context.user_data.get('event', 'не указано')

    # Получаем текущий букет
    bouquet = BOUQUETS[current_bouquet_index]

    bouquet_caption = f"""
    🎀 Идеальный букет для вашего события {user_event}
    {bouquet['description']}
    """

    # Клавиатура для заказа
    order_keyboard = [
        ['Заказать букет'],
        ['Заказать консультацию', 'Посмотреть всю коллекцию']
        ]
    reply_markup = ReplyKeyboardMarkup(order_keyboard, resize_keyboard=True)

    # Отправляем фото букета
    with open(bouquet['photo'], 'rb') as photo_file:
        update.message.reply_photo(
            photo=photo_file,
            caption=bouquet_caption,
            reply_markup=reply_markup)

    # --------код ниже не работает как должно----------
    # update.message.reply_text(
    #     'Для заказа нажмите кнопку ниже:',
    #      reply_markup=reply_markup
    #     )
    # Текст с предложением и две кнопки
    # options_text = (
    #     '**Хотите что-то еще более уникальное?\
    #     Подберите другой букет из нашей коллекции\
    #     или закажите консультацию флориста**'
    #     )
    # options_keyboard = [
    #     ['Заказать консультацию', 'Посмотреть всю коллекцию']
    # ]
    # options_markup = ReplyKeyboardMarkup(
    #     options_keyboard,
    #     resize_keyboard=True
    #     )
    # update.message.reply_text(
    #     options_text,
    #     reply_markup=options_markup,
    #     parse_mode='Markdown'
    #     )


def order_bouquet(update, context):
    """Обработчик кнопки 'Заказать букет'."""
    # Запрашиваем данные для заказа
    context.user_data['order_step'] = 'name'
    update.message.reply_text(
        'Для оформления заказа понадобятся некоторые данные. Как вас зовут?'
    )

    # Создаем клавиатуру для отмены
    cancel_keyboard = [['Отменить заказ']]
    reply_markup = ReplyKeyboardMarkup(cancel_keyboard, resize_keyboard=True)
    update.message.reply_text(
        'Если передумали, нажмите "Отменить заказ"',
        reply_markup=reply_markup
    )

    return ORDER_OPTIONS


def process_order_data(update, context):
    """Обработчик данных заказа."""
    user_data = context.user_data
    current_step = user_data.get('order_step')
    user_text = update.message.text

    if user_text == 'Отменить заказ':
        return cancel_order(update, context)

    if current_step == 'name':
        user_data['customer_name'] = user_text
        user_data['order_step'] = 'address'
        update.message.reply_text('Отлично! Теперь укажите адрес доставки:')

    elif current_step == 'address':
        user_data['address'] = user_text
        user_data['order_step'] = 'date'
        update.message.reply_text(
            'На какую дату нужна доставка? (например, 30.09.2025)'
        )

    elif current_step == 'date':
        user_data['delivery_date'] = user_text
        user_data['order_step'] = 'time'
        update.message.reply_text(
            'В какое время удобно получить заказ? (например, 14:00-16:00)'
        )

    elif current_step == 'time':
        user_data['delivery_time'] = user_text
        # Завершаем сбор данных и отправляем заказ курьеру
        send_order_to_courier(update, context)

        # Показываем опции после заказа
        show_post_order_options(update, context)
        user_data['order_step'] = None
        return ORDER_OPTIONS

    return ORDER_OPTIONS


def send_order_to_courier(update, context):
    """Отправка заказа курьеру."""
    user_data = context.user_data

    order_details = f"""
    🚨 НОВЫЙ ЗАКАЗ БУКЕТА 🚨

    Событие: {user_data.get('event', 'не указано')}
    Бюджет: {user_data.get('budget', 'не указан')}

    Данные клиента:
    Имя: {user_data.get('customer_name', 'не указано')}
    Адрес: {user_data.get('address', 'не указан')}
    Дата доставки: {user_data.get('delivery_date', 'не указана')}
    Время доставки: {user_data.get('delivery_time', 'не указано')}

    Букет: {BOUQUETS[current_bouquet_index]['description']}
    """

    # Отправляем сообщение курьеру
    context.bot.send_message(chat_id=courier_chat_id, text=order_details)

    print(f"Заказ отправлен курьеру: {order_details}")  # Для тестирования

    update.message.reply_text(
        '✅ Ваш заказ принят! Курьер свяжется с вами для подтверждения.'
    )


def show_post_order_options(update, context):
    """Показ опций после заказа."""
    options_text = (
        '**Хотите что-то еще более уникальное? Подберите другой букет из\
        нашей коллекции или закажите консультацию флориста**'
        )
    options_keyboard = [
        ['Заказать консультацию', 'Посмотреть всю коллекцию']
    ]
    options_markup = ReplyKeyboardMarkup(
        options_keyboard,
        resize_keyboard=True
    )

    update.message.reply_text(
        options_text,
        reply_markup=options_markup,
        parse_mode='Markdown'
    )


def order_consultation(update, context):
    """Обработчик кнопки 'Заказать консультацию'."""
    update.message.reply_text(
        'Укажите номер телефона, и наш флорист перезвонит в течение 20 минут.'
    )
    context.user_data['waiting_for_phone'] = True
    return CONSULTATION


def process_consultation_phone(update, context):
    """Обработчик номера телефона."""
    phone_number = update.message.text
    context.user_data['consultation_phone'] = phone_number

    # Отправляем уведомление флористу
    context.bot.send_message(
        chat_id=florist_chat_id,
        text=f'Запрос на консультацию: {phone_number}'
    )

    print(f"Запрос на консультацию: {phone_number}")  # Для тестирования

    update.message.reply_text(
        '✅ Спасибо! Наш флорист свяжется с вами в течение 20 минут.'
    )

    # Возвращаем к основным опциям
    show_post_order_options(update, context)
    context.user_data['waiting_for_phone'] = False
    return ORDER_OPTIONS


def show_collection(update, context):
    """Обработчик кнопки 'Посмотреть всю коллекцию'."""
    global current_bouquet_index
    current_bouquet_index = (current_bouquet_index + 1) % len(BOUQUETS)
    show_bouquet(update, context)
    return ORDER_OPTIONS


def cancel_order(update, context):
    """Отмена заказа."""
    context.user_data['order_step'] = None
    update.message.reply_text('Заказ отменен.')
    show_post_order_options(update, context)
    return ORDER_OPTIONS


if __name__ == '__main__':
    env = Env()
    env.read_env()
    token = env.str('TG_TOKEN')
    courier_chat_id = env.str('CHAT_ID')
    florist_chat_id = env.str('CHAT_ID')
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    updater.start_polling(allowed_updates=['message', 'callback_query'])
    # Создаем обработчик диалога
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_EVENT: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    event_received
                )
            ],
            TYPING_CUSTOM_EVENT: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    custom_event_received
                )
            ],
            CHOOSING_BUDGET: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    budget_received
                )
            ],
            ORDER_OPTIONS: [
                MessageHandler(Filters.regex(
                    '^(Заказать букет)$'),
                    order_bouquet
                ),
                MessageHandler(Filters.regex(
                    '^(Заказать консультацию)$'),
                    order_consultation
                ),
                MessageHandler(Filters.regex(
                    '^(Посмотреть всю коллекцию$)'),
                    show_collection
                ),
                MessageHandler(
                    Filters.text & ~Filters.command,
                    process_order_data
                )
            ],
            CONSULTATION: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    process_consultation_phone
                )
            ]
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    print('Бот запущен и готов к работе!')
    updater.idle()
