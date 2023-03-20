from django.urls import path

urlpatterns = [
    path("credentials", AppCredentialView.as_view(),
         name='get_payment_credentials'),
]
