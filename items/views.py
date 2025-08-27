import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'item.html', {
        'item': item,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY
    })


def create_checkout_session(request, id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)

    item = get_object_or_404(Item, id=id)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),  # Цена в центах
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return JsonResponse({'id': session.id})
    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Внутренняя ошибка сервера'}, status=500)

def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')


def create_payment_intent(request, id):
    item = get_object_or_404(Item, id=id)

    # Получаем ключи для валюты товара
    stripe_keys = settings.STRIPE_KEYS.get(item.currency, settings.STRIPE_KEYS['usd'])

    if not stripe_keys['secret']:
        return JsonResponse({
            'error': f'Stripe API не настроен для валюты {item.currency}'
        }, status=400)

    stripe.api_key = stripe_keys['secret']

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(item.price * 100),
            currency=item.currency,
            metadata={
                'item_id': item.id,
                'item_name': item.name,
            }
        )
        return JsonResponse({
            'client_secret': intent.client_secret,
            'publishable_key': stripe_keys['publishable']
        })
    except Exception as e:
        return JsonResponse({'error': str(e)})

def item_detail_payment_intent(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, 'item_payment_intent.html', {
        'item': item
    })