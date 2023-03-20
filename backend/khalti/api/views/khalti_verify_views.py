from app.api.services.app_service import AppService
from app.api.permissions.authenticated_app import IsAuthenticatedApp
from khalti.api.serializers.verify_serializers import VerifySerializer
from khalti.api.services.khalti_service import KhaltiService

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from utils.helpers import get_client_ip


class KhaltiVerifyView(generics.GenericAPIView):
    """ View for verifying khalti's payment

    Args:
        generics (GenericAPIView): GenericAPIView

    Returns:
        Response: Whether payment is success or not
    """
    authentication_classes = [IsAuthenticatedApp]
    throttle_classes = [UserRateThrottle]
    serializer_class = VerifySerializer

    service = None

    def __init__(self) -> None:
        super().__init__()
        self.service = KhaltiService()

    def get(self, request):
        """Get List Of Payment Available For App

        Args:
            request (request): django request

        Returns:
            list:
        """
        log = self.service.create_transaction_log(
            request.app,
            request.GET['credential_type'],
            request.GET['environment'],
            request.GET['amount'],
            request.GET['reference_id'],
            get_client_ip(request),
            request.META['HTTP_USER_AGENT'],
            request.GET['remarks'],
            request.GET
        )

        credential = AppService.get_credential(
            request.app, 'khalti', request.GET.get('credential_type'), request.GET.get('environment'))

        response = self.service.verify_transaction(
            credential, request.GET['reference_id'])

        self.service.update_transaction_log(
            log, response, self.service.getErrorMessage())

        return Response({
            'status': True if response.status_code == 200 else False,
            'data': response.json()
        }, response.status_code)
