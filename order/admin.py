from django.contrib import admin
from .models import Order, ItemOrdered
# Register your models here.


class ItemOrderedInline(admin.TabularInline):
    model = ItemOrdered
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ItemOrderedInline
    ]


admin.site.register(Order, OrderAdmin)
admin.site.register(ItemOrdered)
