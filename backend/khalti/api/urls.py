from django.urls import path

from khalti.api.views.khalti_verify_views import KhaltiVerifyView


urlpatterns = [
    path("verify", KhaltiVerifyView.as_view(),
         name='verify_khalti_payment'),
]
