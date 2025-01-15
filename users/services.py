import os

import stripe
a = "sk_test_51QQl1iEFB10ARY4qwq5uWxlPiq1YZOBWdcIyot440dS0JSEQFMlQazLNQZ9MxZGPWA50PCokhTVyQZkYCPOiZAJD00Uz6diqG2"
stripe.api_key = os.getenv('SECRET_KEY_API', a)


def create_stripe_product(course):
    """Создает продукт в Stripe, связанный с курсом."""
    product = stripe.Product.create(
        name=course.title,
        description=course.description,
    )
    return product


def create_stripe_price(amount, product_id):
    """Создает цену в Stripe."""
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    price = stripe.Price.create(
        unit_amount=int(amount * 100),  # Убедитесь, что сумма в копейках
        currency="rub",
        product=product_id,
    )
    return price


def create_stripe_session(price_id):
    """Создает сессию в Stripe."""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],  # Убедитесь, что Вы указали количество
        mode="payment",  # Для однократных платежей
        success_url="https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://example.com/cancel",
    )
    return session.id, session.url
