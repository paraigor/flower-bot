import telegram
from django.conf import settings


bot = telegram.Bot(settings.BOT_TOKEN)


def send_order(order):
    bot.send_message(
        chat_id=settings.COURIER_ID,
        text=f"""
Заказ №{order.id}:
Букет: {order.bunch.title}

Цена: {order.bunch.price}

Доставка:
{order.delivery_date} в {order.delivery_time}
Адрес: {order.delivery_address}
Комментарий: {order.comment}

Номер телефона:
{order.client.phone_number}""",
    )