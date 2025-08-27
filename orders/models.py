from django.db import models
from items.models import Item

class Discount(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    percent_off = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процент скидки")
    stripe_coupon_id = models.CharField(max_length=100, blank=True, verbose_name="Stripe Coupon ID")

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        return self.name

class Tax(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процент налога")
    stripe_tax_rate_id = models.CharField(max_length=100, blank=True, verbose_name="Stripe Tax Rate ID")

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"

    def __str__(self):
        return self.name

class Order(models.Model):
    items = models.ManyToManyField(Item, verbose_name="Товары")
    discount = models.ForeignKey(
        Discount,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Скидка"
    )
    tax = models.ForeignKey(
        Tax,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Налог"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id}"

    def get_total_price(self):
        """Рассчитать общую стоимость заказа"""
        total = sum(item.price for item in self.items.all())
        if self.discount:
            total = total * (1 - self.discount.percent_off / 100)
        return round(total, 2)

    def get_items_currency(self):
        """Получить валюту всех товаров (должна быть одинаковой)"""
        currencies = list(set(item.currency for item in self.items.all()))
        if len(currencies) == 1:
            return currencies[0]
        return 'usd'  # по умолчанию