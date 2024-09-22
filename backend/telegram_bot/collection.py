from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    Updater,
)

from .db_querrys import get_bunch_elements, get_random_bunch


def show_random_bunch(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    bunch = get_random_bunch()

    chat_id = query.message.chat_id
    message_id = query.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    image_url = bunch.image.name
    bunch_elements = ""
    for element in get_bunch_elements(bunch):
        bunch_elements += f"{element.element.title} - {element.quantity} шт\n"

    caption = f"""
{bunch.caption}

Состав:
{bunch_elements}
Цена: {bunch.price} рублей
    """
    context.user_data["bunch_for_order"] = bunch
    button = [
        [InlineKeyboardButton("Заказать букет", callback_data="order_start")],
    ]

    context.bot.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(button),
    )

    next_message = """
*Хотите что\-то еще более уникальное\?\n Подберите другой букет из нашей \
коллекции или закажите консультацию флориста\.*
    """
    next_buttons = [
        [
            InlineKeyboardButton(
                "Показать еще", callback_data="show_collection"
            )
        ],
        [
            InlineKeyboardButton(
                "Заказать консультацию", callback_data="request_consultation"
            )
        ],
    ]
    context.bot.send_message(
        text=next_message,
        chat_id=chat_id,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=InlineKeyboardMarkup(next_buttons),
    )


def handlers_register(updater: Updater):
    updater.dispatcher.add_handler(
        CallbackQueryHandler(
            show_random_bunch, pattern="^show_collection$"
        )
    )
    return updater.dispatcher
