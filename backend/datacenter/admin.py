from django.contrib import admin

from .send_order_courier import send_order
from .models import Budget, Bunch, BunchElement, Client, Motive, Order


class BunchElementInline(admin.TabularInline):
    model = Bunch.elements.through
    extra = 0


@admin.register(Bunch)
class BunchAdmin(admin.ModelAdmin):
    inlines = [BunchElementInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['status', 'date', 'client']
    actions = ['send_courier']

    @admin.action(description='Отправить курьеру')
    def send_courier(self, requests, queryset):
        for object in queryset:
            object.status = 'confirmed'
            object.save()
            send_order(object)


admin.site.register(BunchElement)
admin.site.register(Budget)
admin.site.register(Client)
admin.site.register(Motive)

