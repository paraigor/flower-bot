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
    Filters,
    MessageHandler,
    Updater,
)

from .db_querrys import check_and_add_phone_number


def request_phone_number(update: Update, context: CallbackContext):
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
        text="""
Укажите номер телефона, и наш флорист перезвонит вам в течение 20 минут.
Нажмите на кнопку снизу, либо предоставьте контакт клиента
        """,
        reply_markup=ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=True
        ),
    )


def get_ph_number(update: Update, context: CallbackContext):
    user = update.message.contact
    chat_id = update.effective_chat.id
    if update.message.contact:
        ReplyKeyboardRemove(True)
        context.user_data["get_number_in_progress"] = False
        context.user_data["client_id"] = user.user_id
        check_and_add_phone_number(user.user_id, user.phone_number)

    message = """
Флорист скоро свяжется с вами.
А пока можете присмотреть что-нибудь из готовой коллекции.
    """
    button = [
        [
            InlineKeyboardButton(
                "Посмотреть всю коллекцию", callback_data="show_collection"
            )
        ],
    ]
    context.bot.send_message(
        text=message,
        chat_id=chat_id,
        reply_markup=InlineKeyboardMarkup(button),
    )

    context.bot.send_message(
        text=f"""
Клиент {user.first_name} {user.last_name} просит проконсультировать\
по поводу букета\n
Телефон: {user.phone_number}
        """,
        chat_id=settings.FLORIST_ID,
    )


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(
        MessageHandler(Filters.contact & ~Filters.command, get_ph_number)
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(
            request_phone_number, pattern="^request_consultation$"
        )
    )
    return updater.dispatcher
