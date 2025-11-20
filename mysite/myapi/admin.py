import stripe
from django import forms
from django.contrib import admin

from .models import Item, Order, OrderItem, Tax, Discount

models = [Item, Order, OrderItem, Discount]
admin.site.register(models)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):

    fields = ('name', 'percentage')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['stripe_tax_rate_id']
        return []

    def save_model(self, request, obj, form, change):
        if not change and not obj.stripe_tax_rate_id:
            tax_rate = stripe.TaxRate.create(
                display_name=obj.name,
                percentage=float(obj.percentage),
                inclusive=False,
            )
            obj.stripe_tax_rate_id = tax_rate.id

        super().save_model(request, obj, form, change)
