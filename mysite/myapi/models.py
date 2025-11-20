from django.db import models
from django.db.models import F, Sum


class Tax(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    stripe_tax_rate_id = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"


class Discount(models.Model):
    name = models.CharField(max_length=100)
    coupon_id = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('eur', 'EUR'),
        ('rub', 'RUB'),
    ]

    name = models.CharField(max_length=60)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, default='usd')
    tax = models.ForeignKey(
        Tax, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(
        Item, through="OrderItem", related_name="orders")
    tax = models.ForeignKey(
        Tax, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL, null=True, blank=True)

    def total_amount(self):
        result = self.order_items.aggregate(
            total=Sum(F('quantity') * F('item__price')))
        return result['total']

    def __str__(self):
        return f"Заказ №{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='order_items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def line_total(self):
        return self.quantity * self.item.price

    def __str__(self):
        return f"Заказ №{self.order.id} - {self.item.name} x {self.quantity}"
