from rest_framework import generics
from rest_framework.throttling import UserRateThrottle

from drf_yasg.utils import swagger_auto_schema
from utils.helpers import get_client_ip

from app.api.services.app_service import AppService
from app.api.permissions.authenticated_app import IsAuthenticatedApp
from esewa.api.serializers.esewa_verify_serializer import EsewaVerifySerializer
from esewa.api.services.esewa_service import EsewaService


class EsewaPaymentView(generics.GenericAPIView):
    """ View for payment payhment

    Args:
        generics (GenericAPIView): GenericAPIView

    Returns:
        Response: Whether payment is success or not
    """

    throttle_classes = [UserRateThrottle]

    service = None

    def __init__(self) -> None:
        super().__init__()
        self.service = EsewaService()

    @swagger_auto_schema(
        request_body=EsewaVerifySerializer,
        responses={
            200: "Redirects to esewa webpage"
        }
    )
    def post(self, request):
        """Esewa webpayment view

            Args:
                request (request): django request

            Returns:
                Redirect: redirects to esewa payment webpage
        """
        self.service.create_transaction_log(
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

        credential = AppService.get_credential(
            request.app, 'esewa', request.GET['credential_type'], request.GET['environment'])
        return self.service.payment_transaction(request, credential, request.GET)
