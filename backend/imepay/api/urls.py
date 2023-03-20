from django.urls import path
from imepay.api.views.imepay_payment_views import ImepayPaymentView
from imepay.api.views.imepay_web_callback_views import ImePayWebCallback
from imepay.api.views.imepay_verify_views import PaymentVerifyView


urlpatterns = [
    path("payment", ImepayPaymentView.as_view(),name='imepayment'),
    path('web/callback/',ImePayWebCallback.as_view(), name="imepay_web_callback"),
    path('verify',PaymentVerifyView.as_view(),name="verify-payment")

]
