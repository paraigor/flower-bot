import logging

from django.conf import settings
from telegram.ext import Updater

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(settings.BOT_TOKEN, use_context=True)
    updater.start_polling()
    updater.idle()
