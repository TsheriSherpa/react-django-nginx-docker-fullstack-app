from django.urls import path

from esewa.api.views.esewa_payment_views import EsewaPaymentView
from esewa.api.views.esewa_web_callback_views import EsewaWebCallback
from esewa.api.views.esewa_mobile_callback_views import EsewaMobileCallback
from esewa.api.views.esewa_verify_views import EsewaVerifyView
urlpatterns = [
    path("payment", EsewaPaymentView.as_view(),
         name='esewapayment'),
    path("verify",EsewaVerifyView.as_view(),name="esewa_mobile_verify"),
    path('web/callback/<status>',EsewaWebCallback.as_view(), name="esewa_web_callback"),
    path('mobile/callback',EsewaMobileCallback.as_view(),name="esewa_mobile_callback")
]
