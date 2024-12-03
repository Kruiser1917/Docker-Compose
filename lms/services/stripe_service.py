import stripe

stripe.api_key = "4242424242424242"  # Замените на ваш ключ

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

def create_checkout_session(price_id, success_url, cancel_url):
    """
    Создание сессии оплаты в Stripe.
    """
    return stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": price_id,
            "quantity": 1,
        }],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
