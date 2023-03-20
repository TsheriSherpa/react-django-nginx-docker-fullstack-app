from django.urls import path
from prabhupay.api.views import WebPaymentView, PaymentVerifyView

urlpatterns = [
    path("payment/web", WebPaymentView.as_view()),
    path("payment/verify", PaymentVerifyView.as_view()),
]
