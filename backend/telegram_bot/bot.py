import logging

from django.conf import settings
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from .common_functions import build_button_table
from .db_querrys import check_client, create_client, get_motives

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

URL_AGREEMENT = "https://disk.yandex.ru/i/8a4x4M9KB8A3qw"


# Согласие на обработку ПД
def prestart_PD_request(update: Update, context: CallbackContext):
    context.user_data["user_initial"] = update.message.from_user
    button = [[InlineKeyboardButton("Согласен", callback_data="reg_user")]]
    welcome_message = f"""
    Добро пожаловать в бота магазина цветов\!

    Для продолжения работы с ботом нам потребуется Ваше согласие на обработку персональных данных\.
    С документом Вы можете ознакомиться [по ссылке]({URL_AGREEMENT})\.
    Нажимая "Согласен" \- Вы даёте своё согласие и можете продолжать пользоваться ботом\.
    """
    update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(button),
    )


# Регистрация пользователя
def reg_user(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = context.user_data["user_initial"]
    if not check_client(user["id"]):
        create_client(
            user["id"],
            user["first_name"],
            user["last_name"],
            user["username"],
        )
    context.user_data["client_id"] = user["id"]
    start(update, context)


# Старт бота
# Если пользователя нет в бд - согласие ПД, регистрация
def start(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data.clear()
    context.user_data["client_id"] = update.effective_chat.id
    if not check_client(context.user_data["client_id"]):
        prestart_PD_request(update, context)
        return

    motives = get_motives()

    buttons = [
        InlineKeyboardButton(
            motive.title,
            callback_data=f"motive_id_{motive.id}",
        )
        for motive in motives
    ]
    buttons = build_button_table(buttons, cols=2)
    buttons.append(
        [InlineKeyboardButton("Другой повод", callback_data="custom_motive")]
    )

    start_message = """
    Добро пожаловать в бота магазина цветов\!

    Закажите доставку праздничного букета, собранного специально для ваших любимых, родных и коллег\. Наш букет со смыслом станет главным подарком на вашем празднике\.

    *К какому событию готовимся\? Выберите один из вариантов\.*
    """

    if query:
        query.answer()
        query.edit_message_text(
            start_message,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        update.message.reply_text(
            start_message,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


def request_custom_motive(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text("Укажите повод:")


def request_budget(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data["motive"] = (
        update.message.text if update.message else query.data
    )
    
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


def main():
    updater = Updater(settings.BOT_TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(start, pattern="^start$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(reg_user, pattern="^reg_user$")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(request_budget, pattern="^motive_id_")
    )
    updater.dispatcher.add_handler(
        CallbackQueryHandler(request_custom_motive, pattern="^custom_motive$")
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, request_budget)
    )
    updater.start_polling()
    updater.idle()
