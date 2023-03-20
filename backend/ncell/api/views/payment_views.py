from app.api.services.app_service import AppService
from app.api.permissions.authenticated_app import IsAuthenticatedApp
from ncell.api.serializers.payment_serializer import PaymentSerializer

from rest_framework import generics
from rest_framework.throttling import UserRateThrottle
from ncell.api.services.ncell_service import NcellService
from utils.api_response import ApiResponse

from utils.helpers import get_client_ip, get_error_message


class PaymentView(generics.GenericAPIView):
    """ Initiate Ncell Payment

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
        """ Initiate Ncell Payment

        Args:
            request (request): django request

        Returns:
            response: Django Rest Framework Response
        """
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return ApiResponse.send_error(get_error_message(serializer), 400)

        credential = AppService.get_credential(
            request.app, 'ncell',
            request.data['credential_type'],
            request.data['environment']
        )

        log = NcellService.create_transaction_log(
            request.app,
            request.data['credential_type'],
            request.data['environment'],
            request.data['amount'],
            request.data['reference_id'],
            get_client_ip(request),
            request.META['HTTP_USER_AGENT'],
            request.data['remarks'],
            request.data
        )

        consent_url = NcellService.initiate_payment(credential, log)
        print(consent_url)

        if not consent_url:
            return ApiResponse.send_error(NcellService.getErrorMessage(), NcellService.getErrorCode())

        return ApiResponse.send_success(consent_url)
