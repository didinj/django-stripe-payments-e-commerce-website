from django.urls import path
from .views import CreateCheckoutSessionView, stripe_webhook, success_view, cancel_view

urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success/', success_view, name='success'),
    path('cancel/', cancel_view, name='cancel'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
]