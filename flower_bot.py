import os
import random

from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, \
    MessageHandler, Filters, ConversationHandler

EVENT, BUDGET, CUSTOM_EVENT, NAME, ADDRESS, DATE, TIME, PHONE_NUMBER = range(8)

COURIER_ID = '2082099178'
FLORIST_ID = '3055049156'

bouquets = [
    {
        "image": "https://clck.ru/3DPm5Y",
        "description": "Этот букет несет в себе всю нежность ваших чувств!",
        "composition": "Розы, лилии, зелень",
        "price": "1000 рублей"
    },
    {
        "image": "https://clck.ru/3DPkuB",
        "description": "Яркий и насыщенный букет для любого праздника!",
        "composition": "Герберы, хризантемы, зелень",
        "price": "1500 рублей"
    },
    {
        "image": "https://clck.ru/3DPmsT",
        "description": "Нежный букет для тех, кто ценит простоту.",
        "composition": "Полевые цветы, зелень",
        "price": "500 рублей"
    },
    {
        "image": "https://clck.ru/3DPmy7",
        "description": "Элегантный букет для особых моментов.",
        "composition": "Орхидеи, розы, зелень",
        "price": "2000 рублей"
    },
    {
        "image": "https://clck.ru/3DPn74",
        "description": "Яркий букет, чтобы поднять настроение.",
        "composition": "Тюльпаны, нарциссы, зелень",
        "price": "1500 рублей"
    },
    {
        "image": "https://clck.ru/3DPnB5",
        "description": "Роскошный букет для истинных ценителей.",
        "composition": "Розы, гортензии, зелень",
        "price": "2500 рублей"
    },
]

# Функция приветствия
def start_welcome(update: Update, context):
    keyboard = [
        [InlineKeyboardButton('День рождения', callback_data='День рождения'),
         InlineKeyboardButton('Свадьба', callback_data='Свадьба')],
        [InlineKeyboardButton('В школу', callback_data='В школу'),
         InlineKeyboardButton('Юбилей', callback_data='Юбилей')],
        [InlineKeyboardButton('Без повода', callback_data='Без повода'),
         InlineKeyboardButton('Другой повод', callback_data='Другой повод')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Доброго времени суток! К какому событию готовимся? Выберите один из вариантов, либо укажите свой:",
        reply_markup=reply_markup
    )
    return EVENT

# Функция выбора повода
def event_selection(update: Update, context):
    query = update.callback_query
    query.answer()
    event = query.data

    if event == "Другой повод":
        query.message.reply_text("Введите ваше событие:")
        return CUSTOM_EVENT

    context.user_data['event'] = event
    return ask_budget(query, context)


def custom_event_input(update: Update, context):
    custom_event = update.message.text
    context.user_data['event'] = custom_event
    return ask_budget(update, context)


def ask_budget(update: Update, context):
    keyboard = [
        [InlineKeyboardButton('~500', callback_data='~500'),
         InlineKeyboardButton('~1000', callback_data='~1000')],
        [InlineKeyboardButton('~2000', callback_data='~2000'),
         InlineKeyboardButton('Больше', callback_data='Больше')],
        [InlineKeyboardButton('Не важно', callback_data='Не важно')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if hasattr(update, 'message'):
        update.message.reply_text(
            f"Вы выбрали: {context.user_data['event']}. На какую сумму рассчитываете?",
            reply_markup=reply_markup
        )
    elif hasattr(update, 'callback_query'):
        update.callback_query.edit_message_text(
            f"Вы выбрали: {context.user_data['event']}. На какую сумму рассчитываете?",
            reply_markup=reply_markup
        )

    return BUDGET


def budget_selection(update: Update, context):
    query = update.callback_query
    query.answer()
    budget = query.data
    context.user_data['budget'] = budget

    budget_mapping = {
        '~500': [bouquets[2]],
        '~1000': [bouquets[0]],
        '~1500': [bouquets[1], bouquets[4]],
        '~2000': [bouquets[3]],
        'Больше': [bouquets[5]],
        'Не важно': bouquets
    }

    selected_bouquets = budget_mapping.get(budget, [])
    bouquet = random.choice(selected_bouquets)

    query.edit_message_text(
        f"Ваш бюджет: {budget}. Вот подходящий букет для вас:\n\n"
        f"{bouquet['description']}\n"
        f"Состав: {bouquet['composition']}\n"
        f"Стоимость: {bouquet['price']}"
    )

    query.bot.send_photo(chat_id=query.message.chat_id, photo=bouquet['image'])

    keyboard = [
        [InlineKeyboardButton('Заказать букет', callback_data='order')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.bot.send_message(chat_id=query.message.chat_id,
                           text="Если вы хотите заказать букет, нажмите кнопку ниже:",
                           reply_markup=reply_markup)

    if not context.user_data.get('bold_text_sent'):
        bold_text = "**Хотите что-то еще более уникальное? Подберите другой букет из нашей коллекции или закажите консультацию флориста**"
        query.bot.send_message(chat_id=query.message.chat_id, text=bold_text,
                               parse_mode='Markdown')

        keyboard = [
            [InlineKeyboardButton('Заказать консультацию',
                                  callback_data='consultation'),
             InlineKeyboardButton('Посмотреть всю коллекцию',
                                  callback_data='collection')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.bot.send_message(chat_id=query.message.chat_id,
                               text="Выберите вариант:",
                               reply_markup=reply_markup)

        context.user_data['bold_text_sent'] = True

    return ConversationHandler.END


def order_bouquet(update: Update, context):
    query = update.callback_query
    query.answer()

    context.bot.send_message(chat_id=query.message.chat_id,
                             text="Отлично! Давайте оформим ваш заказ. Для начала, пожалуйста, введите ваше имя.")

    return NAME


def get_name(update: Update, context):
    context.user_data['name'] = update.message.text
    update.message.reply_text(
        "Спасибо! Теперь, пожалуйста, введите адрес доставки.")
    return ADDRESS


def get_address(update: Update, context):
    context.user_data['address'] = update.message.text
    update.message.reply_text(
        " Укажите дату доставки в формате ДД.ММ.ГГГГ.")
    return DATE


def get_date(update: Update, context):
    context.user_data['date'] = update.message.text
    update.message.reply_text(
        " Укажите желаемое время доставки в формате ЧЧ:ММ.")
    return TIME


def get_time(update: Update, context):
    context.user_data['time'] = update.message.text

    # Сообщение для курьера
    courier_message = f"Новый заказ!\n\n" \
                      f"Имя: {context.user_data['name']}\n" \
                      f"Адрес: {context.user_data['address']}\n" \
                      f"Дата: {context.user_data['date']}\n" \
                      f"Время: {context.user_data['time']}\n" \
                      f"Событие: {context.user_data['event']}\n" \
                      f"Бюджет: {context.user_data['budget']}"

    # Отправка сообщение курьеру
    context.bot.send_message(chat_id=COURIER_ID, text=courier_message)

    # Подтверждение заказа пользователю
    update.message.reply_text(
        "Спасибо за ваш заказ! Мы передали информацию курьеру. Ожидайте доставку в указанное время.")

    return ConversationHandler.END


def cancel(update: Update, context):
    update.message.reply_text(
        "Операция отменена. Если понадобится помощь, обращайтесь!")
    return ConversationHandler.END


# Обработка запроса на консультацию
def consultation_request(update: Update, context):
    query = update.callback_query
    query.answer()

    query.message.reply_text(
        "Укажите номер телефона, и наш флорист перезвонит вам в течение 20 минут.")
    return PHONE_NUMBER


def get_phone_number(update: Update, context):
    phone_number = update.message.text
    context.user_data['phone_number'] = phone_number

    update.message.reply_text(
        "Флорист скоро свяжется с вами. А пока можете присмотреть что-нибудь из готовой коллекции."
    )

    # Отправка нового букета и интерфейса
    bouquet = random.choice(bouquets)
    update.message.reply_text(
        f"Вот подходящий букет для вас:\n\n"
        f"{bouquet['description']}\n"
        f"Состав: {bouquet['composition']}\n"
        f"Стоимость: {bouquet['price']}"
    )
    context.bot.send_photo(chat_id=update.message.chat_id,
                           photo=bouquet['image'])

    keyboard = [
        [
            InlineKeyboardButton('Заказать букет', callback_data='order'),
            InlineKeyboardButton('Посмотреть всю коллекцию',
                                 callback_data='collection')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Выберите вариант:",
                             reply_markup=reply_markup)

    return ConversationHandler.END


def view_collection(update: Update, context):
    query = update.callback_query
    query.answer()

    # Отправка нового букета из коллекции
    bouquet = random.choice(bouquets)
    query.message.reply_text(
        f"Вот подходящий букет для вас:\n\n"
        f"{bouquet['description']}\n"
        f"Состав: {bouquet['composition']}\n"
        f"Стоимость: {bouquet['price']}"
    )
    context.bot.send_photo(chat_id=query.message.chat_id,
                           photo=bouquet['image'])

    keyboard = [
        [
            InlineKeyboardButton('Заказать букет', callback_data='order'),
            InlineKeyboardButton('Следующее фото', callback_data='collection')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=query.message.chat_id,
                             text="Выберите вариант:",
                             reply_markup=reply_markup)


def main():
    load_dotenv()
    telegram_bot_token = os.environ['YOUR_TG_TOKEN']

    updater = Updater(telegram_bot_token, use_context=True)
    dp = updater.dispatcher

    # Обработчики
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_welcome)],
        states={
            EVENT: [CallbackQueryHandler(event_selection)],
            CUSTOM_EVENT: [MessageHandler(Filters.text & ~Filters.command,
                                          custom_event_input)],
            BUDGET: [CallbackQueryHandler(budget_selection)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    order_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(order_bouquet, pattern='^order$')],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            ADDRESS: [
                MessageHandler(Filters.text & ~Filters.command, get_address)],
            DATE: [MessageHandler(Filters.text & ~Filters.command, get_date)],
            TIME: [MessageHandler(Filters.text & ~Filters.command, get_time)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Обработчик для консультаций
    consultation_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(consultation_request,
                                           pattern='^consultation$')],
        states={
            PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command,
                                          get_phone_number)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(order_handler)
    dp.add_handler(consultation_handler)
    dp.add_handler(
        CallbackQueryHandler(view_collection, pattern='^collection$'))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
