from django.contrib import admin

from .models import Budget, Bunch, BunchElement, Client, Motive, Order


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
