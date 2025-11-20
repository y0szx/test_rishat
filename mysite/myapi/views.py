import os
import stripe
from dotenv import load_dotenv
from rest_framework import viewsets
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import Item, Order
from .serializers import ItemSerializer

load_dotenv()

secret_api_key = os.getenv("SECRET_API_KEY")
publishable_api_key = os.getenv("PUBLISHABLE_API_KEY")
base_url = os.getenv("SERVER_BASE_URL")
stripe.api_key = secret_api_key


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('name')
    serializer_class = ItemSerializer


def item_detail(request, id):
    item = get_object_or_404(Item, pk=id)
    return render(request, "item_details.html", {"publishable_key": publishable_api_key, "item": item})


def order_detail(request, id):
    order = get_object_or_404(Order, pk=id)
    return render(request, "order_details.html", {"publishable_key": publishable_api_key, "order": order})


def success(request):
    return render(request, "success.html")


def buy_item(request, id):
    item = get_object_or_404(Item, pk=id)

    amount_cents = int(item.price * 100)

    tax = []

    if item.tax:
        tax.append(item.tax.stripe_tax_rate_id)

    line_items = [
        {
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                    'description': item.description,
                },
                'unit_amount': amount_cents,
            },
            'quantity': 1,
            'tax_rates': tax,
        }
    ]

    session_data = {
        'line_items': line_items,
        'mode': 'payment',
        'success_url': f'{base_url}/success/'
    }

    if item.discount:
        session_data['discounts'] = [{'coupon': item.discount.coupon_id}]

    session = stripe.checkout.Session.create(**session_data)

    return JsonResponse({'sessionId': session.id})


def buy_order(request, id):
    order = get_object_or_404(Order, pk=id)

    tax = []

    if order.tax:
        tax.append(order.tax.stripe_tax_rate_id)

    line_items = []
    for order_item in order.order_items.all():
        line_items.append({
            'price_data': {
                'currency': order_item.item.currency,
                'product_data': {
                    'name': order_item.item.name,
                    'description': order_item.item.description,
                },
                'unit_amount': int(order_item.item.price * 100),
            },
            'quantity': order_item.quantity,
            'tax_rates': tax,
        })

    session_data = {
        'line_items': line_items,
        'mode': 'payment',
        'success_url': f'{base_url}/success/'
    }

    if order.discount:
        session_data['discounts'] = [{'coupon': order.discount.coupon_id}]

    session = stripe.checkout.Session.create(**session_data)

    return JsonResponse({'sessionId': session.id})
