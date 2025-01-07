import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# stripe.api_key = "4242424242424242"  # Замените на ваш ключ

def create_product(name):
    """
    Создание продукта в Stripe.
    """
    return stripe.Product.create(name=name)

def create_price(product_id, amount):
    """
    Создание цены для продукта в Stripe.
    Цена передается в копейках (например, 10000 для 100.00).
    """
    return stripe.Price.create(
        unit_amount=amount,
        currency="usd",
        product=product_id,
    )

import stripe
from django.conf import settings

# Устанавливаем ключ Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(data):
    """
    Создаёт сессию для оплаты через Stripe.
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': data.get('product_name', 'Product')},
                        'unit_amount': int(data.get('price', 1000)) * 100,  # Умножаем на 100, так как Stripe принимает цену в центах
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=data.get('success_url', 'http://localhost:8000/success/'),
            cancel_url=data.get('cancel_url', 'http://localhost:8000/cancel/'),
        )
        return session.url
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {e.user_message}")
