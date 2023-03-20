from django.urls import path

from stripe_card.api import views


urlpatterns = [
    path("payment", views.PaymentView.as_view(),
         name='make_stripe_payment'),
    path("create-payment-intent", views.CreatePaymentIntentView.as_view(),
         name='make_stripe_payment'),
    path("verify-payment", views.VerifyPaymentIntentView.as_view())
]
