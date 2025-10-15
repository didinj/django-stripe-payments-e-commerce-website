import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from products.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY

def handle_successful_payment(session):
    Order.objects.create(
        session_id=session['id'],
        amount_total=session['amount_total'] / 100,
        email=session['customer_details']['email'],
        paid=True
    )
    print(f"✅ Order created for {session['customer_details']['email']}")

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'your-webhook-signing-secret'  # Replace with your actual secret
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_successful_payment(session)

    return HttpResponse(status=200)

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})
        line_items = []

        for product_id, item in cart.items():
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': item['name']},
                    'unit_amount': int(item['price'] * 100),
                },
                'quantity': item['quantity'],
            })

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL,
        )

        return redirect(session.url, code=303)
    
    def success_view(request):
        request.session['cart'] = {}  # clear the cart after payment
        return render(request, 'payments/success.html')

    def cancel_view(request):
        return render(request, 'payments/cancel.html')
