from app.api.services.app_service import AppService
from app.api.permissions.authenticated_app import IsAuthenticatedApp
from fonepay.api.serializers.payment_serializer import PaymentSerializer

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from fonepay.api.services.fonepay_service import FonepayService
from utils.api_response import ApiResponse

from utils.helpers import get_client_ip


class PaymentView(generics.GenericAPIView):
    """ Initiate fonepay web payment

    Args:
        generics (GenericAPIView): GenericAPIView

    Returns:
        Response: Django rest framework response 
    """
    authentication_classes = [IsAuthenticatedApp]
    throttle_classes = [UserRateThrottle]
    serializer_class = PaymentSerializer

    service = None

    def __init__(self) -> None:
        super().__init__()

    def post(self, request):
        """ Initiate fonepay payment

        Args:
            request (request): django request

        Returns:
            response: Django Rest Framework Response
        """
        credential = AppService.get_credential(
            request.app, 'fonepay',
            request.data['credential_type'],
            request.data['environment']
        )

        log = FonepayService.create_transaction_log(
            request.app,
            request.data['credential_type'],
            request.data['environment'],
            request.data['amount'],
            request.data['reference_id'],
            get_client_ip(request),
            request.META['HTTP_USER_AGENT'],
            request.data['remarks'],
            request.data['app_payload'],
            request.data['app_api'],
            request.data
        )

        payment_url = FonepayService.initiate_payment(credential, log)
        return ApiResponse.send_success(payment_url)
