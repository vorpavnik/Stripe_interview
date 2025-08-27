from django.contrib import admin
from .models import Order, Discount, Tax

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)
    list_display = ['id']
    filter_vertical = ['items']

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'percent_off']

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'percentage']