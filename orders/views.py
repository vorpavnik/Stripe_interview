import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Order


def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    currency = order.get_items_currency()

    # Получаем ключи для валюты
    stripe_keys = settings.STRIPE_KEYS.get(currency, settings.STRIPE_KEYS['usd'])
    publishable_key = stripe_keys['publishable']

    return render(request, 'order.html', {
        'order': order,
        'STRIPE_PUBLISHABLE_KEY': publishable_key,
        'currency': currency
    })


def create_order_checkout_session(request, id):
    order = get_object_or_404(Order, id=id)
    currency = order.get_items_currency()

    # Получаем ключи для валюты
    stripe_keys = settings.STRIPE_KEYS.get(currency, settings.STRIPE_KEYS['usd'])

    if not stripe_keys['secret']:
        return JsonResponse({
            'error': f'Stripe API не настроен для валюты {currency}'
        }, status=400)

    stripe.api_key = stripe_keys['secret']

    try:
        # Создаем line items для всех товаров
        line_items = []
        for item in order.items.all():
            line_items.append({
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            })

        # Параметры сессии
        session_params = {
            'payment_method_types': ['card'],
            'line_items': line_items,
            'mode': 'payment',
            'success_url': request.build_absolute_uri('/success/'),
            'cancel_url': request.build_absolute_uri('/cancel/'),
        }

        # Добавляем налоги если есть
        if order.tax and order.tax.stripe_tax_rate_id:
            session_params['line_items'][0]['tax_rates'] = [order.tax.stripe_tax_rate_id]

        # Добавляем скидку если есть
        if order.discount and order.discount.stripe_coupon_id:
            session_params[' discounts'] = [{'coupon': order.discount.stripe_coupon_id}]

        session = stripe.checkout.Session.create(**session_params)
        return JsonResponse({'id': session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)})