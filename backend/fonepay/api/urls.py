from django.urls import path

from fonepay.api.views import PaymentView, PaymentCallbackView


urlpatterns = [
    path("payment", PaymentView.as_view(),
         name='initiate_fonepay_payment'),
    path("payment/callback", PaymentCallbackView.as_view(),
         name='payment_callback'),
]
