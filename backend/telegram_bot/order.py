import datetime as dt

from django.conf import settings
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from .common_functions import build_button_table
from .db_querrys import (
    check_and_add_phone_number,
    create_order,
    get_client,
)

COURIER_ID = settings.COURIER_ID
WORKDAY_START = 8
WORKDAY_END = 20


def order_start(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    context.bot.send_message(
        text="Напишите ваше имя:",
        chat_id=update.effective_chat.id,
    )
    return "NAME"


def get_name(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text
    request_delivery_address(update, context)
    return "DELIVERY_ADDRESS"


def request_delivery_address(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text="Напишите адрес доставки:",
    )


def get_delivery_address(update: Update, context: CallbackContext):
    context.user_data["delivery_address"] = update.message.text
    show_delivery_date(update, context)
    return "DELIVERY_DATE"


def show_delivery_date(update: Update, context: CallbackContext):
    today = dt.datetime.today()
    buttons = []

    if dt.datetime.now().hour < WORKDAY_END:
        day_start = 0
    else:
        day_start = 1
    for day in range(day_start, day_start + 9):
        date = today + dt.timedelta(days=day)
        delivery_date = date.strftime("%m-%d")
        buttons.append(
            InlineKeyboardButton(
                delivery_date, callback_data=f"delivery_date_{delivery_date}"
            )
        )
    buttons = build_button_table(buttons, cols=3)

    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text="Выберете дату доставки:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def get_delivery_date(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.user_data["delivery_date"] = query.data.split("_")[-1]
    show_delivery_time(update, context)
    return "DELIVERY_TIME"


def show_delivery_time(update: Update, context: CallbackContext):
    query = update.callback_query
    buttons = []
    delivery_date = context.user_data["delivery_date"]
    current_date = dt.datetime.now()
    delivery_date = f"{current_date.year}-{delivery_date}"
    delivery_date = dt.datetime.strptime(delivery_date, "%Y-%m-%d")
    day_diff = (delivery_date - current_date).total_seconds() / 86400
    current_hour = current_date.hour
    current_minute = current_date.minute
    if WORKDAY_START <= current_hour < WORKDAY_END and day_diff <= 1:
        if current_minute:
            start_hour = current_hour + 1
        else:
            start_hour = current_hour
    else:
        start_hour = WORKDAY_START
    end_hour = WORKDAY_END + 1
    for hour in range(start_hour, end_hour):
        buttons.append(
            InlineKeyboardButton(
                f"{hour:02}:00", callback_data=f"delivery_time_{hour}"
            )
        )
    buttons = build_button_table(buttons, cols=3)

    query.edit_message_text(
        text="Выберете время доставки:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def get_delivery_time(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    context.user_data["delivery_time"] = query.data.split("_")[-1]
    show_comment_fetch(update, context)
    return "COMMENT"


def show_comment_fetch(update, context):
    query = update.callback_query
    query.answer()
    buttons = [
        [InlineKeyboardButton("Пропустить", callback_data="skip_comment")],
    ]

    query.edit_message_text(
        text="Комментарий для курьера:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


def get_comment(update: Update, context: CallbackContext):
    query = update.callback_query
    if query:
        query.answer()
    context.user_data["delivery_comment"] = (
        update.message.text if update.message else ""
    )
    show_phone_number_fetch(update, context)
    return "PHONE_NUMBER"


def show_phone_number_fetch(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = [
        [
            KeyboardButton(
                "Поделиться номером",
                request_contact=True,
            )
        ]
    ]
    if query:
        chat_id = query.message.chat_id
        message_id = query.message.message_id
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text="Укажите Ваш номер телефона с помощью нажатия на кнопку снизу, либо предоставьте контакт клиента",
        reply_markup=ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=True
        ),
    )


def get_phone_number(update: Update, context: CallbackContext):
    user = update.message.contact
    if update.message.contact:
        ReplyKeyboardRemove(True)
        context.user_data["get_number_in_progress"] = False
        context.user_data["client_id"] = user.user_id
        check_and_add_phone_number(user.user_id, user.phone_number)
        make_order(update, context)

    return ConversationHandler.END


def make_order(update: Update, context: CallbackContext):
    bunch = context.user_data["bunch_for_order"]
    client_id = context.user_data["client_id"]
    client = get_client(client_id)
    delivery_comment = context.user_data["delivery_comment"]
    delivery_time = context.user_data["delivery_time"]
    delivery_date = context.user_data["delivery_date"]
    current_year = dt.datetime.today().year
    delivery_date = f"{current_year}-{delivery_date}"
    delivery_address = context.user_data["delivery_address"]
    order = create_order(
        client,
        bunch,
        delivery_date,
        delivery_time,
        delivery_address,
        delivery_comment,
    )
    # send_order(update, context, order)
    order_end(update, context)


# def send_order(update, context, order):
#     context.bot.send_message(
#         chat_id=admin_chat_id,
#         text=f"""
# Заказ №{order.id}:
# Торт: {order.cake.title or 'сборный'}
# Уровни: {order.cake.level.title}
# Форма: {order.cake.form.title}
# Топпинг: {order.cake.topping.title}
# Ягода: {order.cake.berry and order.cake.berry.title or '-'}
# Декор: {order.cake.decor and order.cake.decor.title or '-'}
# Надпись: {order.cake.caption or '-'}

# Цена: {order.invoice.amount}

# Доставка:
# {order.delivery_date} в {order.delivery_time}
# Адрес: {order.delivery_address}
# Комментарий: {order.comment}

# Номер телефона:
# {order.client.phone_number}""",
#     )


def order_end(update: Update, context: CallbackContext):
    query = update.callback_query
    button = [[InlineKeyboardButton("В меню", callback_data="start")]]
    if query:
        query.answer()
        query.edit_message_text(
            text="Заказ принят",
            reply_markup=InlineKeyboardMarkup(button),
        )
    else:
        chat_id = update.effective_chat.id
        context.bot.send_message(
            chat_id=chat_id,
            text="Заказ принят",
            reply_markup=InlineKeyboardMarkup(button),
        )


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CallbackQueryHandler(
                    order_start, pattern="^order_start$"
                )
            ],
            states={
                "NAME": [
                    MessageHandler(
                        Filters.text & ~Filters.command, get_name
                    ),
                ],
                "DELIVERY_ADDRESS": [
                    MessageHandler(
                        Filters.text & ~Filters.command, get_delivery_address
                    ),
                ],
                "DELIVERY_DATE": [
                    CallbackQueryHandler(
                        get_delivery_date, pattern="^delivery_date_"
                    ),
                ],
                "DELIVERY_TIME": [
                    CallbackQueryHandler(
                        get_delivery_time, pattern="^delivery_time_"
                    ),
                ],
                "COMMENT": [
                    CallbackQueryHandler(
                        get_comment, pattern="^skip_comment$"
                    ),
                    MessageHandler(
                        Filters.text & ~Filters.command, get_comment
                    ),
                ],
                "PHONE_NUMBER": [
                    MessageHandler(
                        Filters.contact & ~Filters.command, get_phone_number
                    )
                ],
            },
            fallbacks=[],
        )
    )
    return updater.dispatcher
