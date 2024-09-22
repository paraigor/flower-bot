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
)

admin_chat_id = settings.ADMIN_ID


def get_data_for_cake(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    buttons = [
        [
            InlineKeyboardButton(
                "Пропустить", callback_data="skip_cake_caption"
            )
        ],
        [InlineKeyboardButton("Главное меню", callback_data="start")],
    ]
    try:
        query.edit_message_text(
            text="Хотите сделать надпись на торте? Укажите в сообщении",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception:
        chat_id = query.message.chat_id
        message_id = query.message.message_id
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        context.bot.send_message(
            text="Хотите сделать надпись на торте? Укажите в сообщении",
            reply_markup=InlineKeyboardMarkup(buttons),
            chat_id=update.effective_chat.id,
        )
    return "CAPTION"


def get_cake_caption(update: Update, context: CallbackContext):
    context.user_data["cake_caption"] = (
        update.message.text if update.message else ""
    )
    show_delivery_address(update, context)
    return "DELIVERY_ADDRESS"


def show_delivery_address(update: Update, context: CallbackContext):
    query = update.callback_query
    buttons = [
        [InlineKeyboardButton("Назад", callback_data="get_data_for_cake")],
        [InlineKeyboardButton("Главное меню", callback_data="start")],
    ]
    if query:
        query.answer()
        query.edit_message_text(
            "Напишите в чат адрес доставки",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        chat_id = update.effective_chat.id
        context.bot.send_message(
            chat_id=chat_id,
            text="Напишите в чат адрес доставки",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


def get_delivery_address(update: Update, context: CallbackContext):
    context.user_data["delivery_address"] = update.message.text
    show_delivery_date(update, context)
    return "DELIVERY_DATE"


def show_delivery_date(update: Update, context: CallbackContext):
    # query = update.callback_query
    # chat_id = query.message.chat_id
    # message_id = query.message.message_id
    # context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    today = dt.datetime.today()
    buttons = []

    if dt.datetime.now().hour < WOKRDAY_END:
        day_start = 1
    else:
        day_start = 2
    for day in range(day_start, day_start + 9):
        date = today + dt.timedelta(days=day)
        delivery_date = date.strftime("%m-%d")
        buttons.append(
            InlineKeyboardButton(
                delivery_date, callback_data=f"delivery_date_{delivery_date}"
            )
        )
    buttons = build_button_table(buttons, cols=3)
    buttons.append(
        [InlineKeyboardButton("Назад", callback_data="show_delivery_address")]
    )
    buttons.append(
        [InlineKeyboardButton("Главное меню", callback_data="start")]
    )

    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text=f"""Выберете дату доставки.
Просим учесть, что минимальное время доставки: {MINIMUM_LEDA_TIME} часов
Цена доставки до {MAXIMUM_EXPEDITED_LEAD_TIME} часов будет увеличена на 20%""",
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
    if WORKDAY_START <= current_hour < WOKRDAY_END and day_diff <= 1:
        if current_minute:
            start_hour = current_hour + 1
        else:
            start_hour = current_hour
    else:
        start_hour = WORKDAY_START
    end_hour = WOKRDAY_END + 1
    for hour in range(start_hour, end_hour):
        buttons.append(
            InlineKeyboardButton(
                f"{hour:02}:00", callback_data=f"delivery_time_{hour}"
            )
        )
    buttons = build_button_table(buttons, cols=3)
    buttons.append(
        [InlineKeyboardButton("Назад", callback_data="show_delivery_date")]
    )
    buttons.append(
        [InlineKeyboardButton("Главное меню", callback_data="start")]
    )
    query.edit_message_text(
        text=f"""Выберете время доставки.
Просим учесть, что минимальное время доставки: {MINIMUM_LEDA_TIME} часов
Цена доставки до {MAXIMUM_EXPEDITED_LEAD_TIME} часов будет увеличена на 20%""",
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
    buttons = [
        [InlineKeyboardButton("Пропустить", callback_data="skip_comment")],
        [InlineKeyboardButton("Назад", callback_data="show_delivery_time")],
        [InlineKeyboardButton("Главное меню", callback_data="start")],
    ]
    if query:
        query.answer()
        query.edit_message_text(
            text="Комментарий для курьера",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        chat_id = update.effective_chat.id
        context.bot.send_message(
            chat_id=chat_id,
            text="Комментарий для курьера",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


def get_comment(update: Update, context: CallbackContext):
    query = update.callback_query
    if query:
        query.answer()
    context.user_data["delivery_comment"] = (
        update.message.text if update.message else ""
    )
    show_phone_number(update, context)
    return "PHONE_NUMBER"


def show_phone_number(update: Update, context: CallbackContext):
    query = update.callback_query
    keyboard = [
        [
            KeyboardButton(
                "Поделиться номером",
                request_contact=True,
            )
        ]
    ]
    # chat_id = query.message.chat_id
    # message_id = query.message.message_id
    # context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id,
        text="""Укажите Ваш номер телефона с помощью нажатия на кнопку снизу, либо предоставьте контакт клиента""",
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
    cake = context.user_data["cake_for_order"]
    cake.caption=context.user_data["cake_caption"]
    cake.save()
    client_id = context.user_data["client_id"]
    client = get_client(client_id)
    delivery_comment = context.user_data["delivery_comment"]
    delivery_time = context.user_data["delivery_time"]
    delivery_date = context.user_data["delivery_date"]
    current_year = dt.datetime.today().year
    delivery_date = f"{current_year}-{delivery_date}"
    delivery_address = context.user_data["delivery_address"]
    invoice = create_invoice(client, cake.price, delivery_date, delivery_time)
    order = create_order(
        client,
        cake,
        delivery_date,
        delivery_time,
        delivery_address,
        invoice,
        delivery_comment,
    )
    send_order(update, context, order)
    order_end(update, context)


def send_order(update, context, order):
    context.bot.send_message(
        chat_id=admin_chat_id,
        text=f"""
Заказ №{order.id}:
Торт: {order.cake.title or 'сборный'}
Уровни: {order.cake.level.title}
Форма: {order.cake.form.title}
Топпинг: {order.cake.topping.title}
Ягода: {order.cake.berry and order.cake.berry.title or '-'}
Декор: {order.cake.decor and order.cake.decor.title or '-'}
Надпись: {order.cake.caption or '-'}

Цена: {order.invoice.amount}

Доставка:
{order.delivery_date} в {order.delivery_time}
Адрес: {order.delivery_address}
Комментарий: {order.comment}

Номер телефона:
{order.client.phone_number}""",
    )


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
                    get_data_for_cake, pattern="^get_data_for_cake$"
                )
            ],
            states={
                "CAPTION": [
                    CallbackQueryHandler(
                        get_cake_caption, pattern="^skip_cake_caption$"
                    ),
                    MessageHandler(
                        Filters.text & ~Filters.command, get_cake_caption
                    ),
                ],
                "DELIVERY_ADDRESS": [
                    MessageHandler(
                        Filters.text & ~Filters.command, get_delivery_address
                    ),
                    CallbackQueryHandler(
                        get_data_for_cake, pattern="^get_data_for_cake$"
                    ),
                ],
                "DELIVERY_DATE": [
                    CallbackQueryHandler(
                        get_delivery_date, pattern="^delivery_date_"
                    ),
                    CallbackQueryHandler(
                        show_delivery_address,
                        pattern="^show_delivery_address$",
                    ),
                ],
                "DELIVERY_TIME": [
                    CallbackQueryHandler(
                        get_delivery_time, pattern="^delivery_time_"
                    ),
                    CallbackQueryHandler(
                        show_delivery_date,
                        pattern="^show_delivery_date$",
                    ),
                ],
                "COMMENT": [
                    CallbackQueryHandler(
                        get_comment, pattern="^skip_comment$"
                    ),
                    CallbackQueryHandler(
                        show_delivery_time, pattern="^show_delivery_time$"
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
