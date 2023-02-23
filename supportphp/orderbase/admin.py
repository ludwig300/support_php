from django.contrib import admin

from .models import Client, Maker, Order


@admin.register(Client)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('name', 'subscription_is_active')


@admin.register(Maker)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('name', 'subscription_is_active')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ('order_datetime', 'name', 'client', 'maker', 'order_is_done')
