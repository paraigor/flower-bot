from django.contrib import admin

from .models import Budget, Bunch, BunchElement, Client, Motive, Order

# def send_order():
#     bot.send_message(
#         chat_id=settings.COURIER_ID,
#         text=f"""
# Заказ №{order.id}:
# Букет: {order.bunch.title}

# Цена: {order.bunch.price}

# Доставка:
# {order.delivery_date} в {order.delivery_time}
# Адрес: {order.delivery_address}
# Комментарий: {order.comment}

# Номер телефона:
# {order.client.phone_number}""",
#     )

class BunchElementInline(admin.TabularInline):
    model = Bunch.elements.through
    extra = 0


@admin.register(Bunch)
class BunchAdmin(admin.ModelAdmin):
    inlines = [BunchElementInline]


admin.site.register(BunchElement)
admin.site.register(Budget)
admin.site.register(Client)
admin.site.register(Motive)
admin.site.register(Order)
