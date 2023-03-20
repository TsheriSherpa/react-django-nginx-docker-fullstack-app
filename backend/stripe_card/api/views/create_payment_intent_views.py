from rest_framework import generics
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from app.api.permissions.authenticated_app import IsAuthenticatedApp
from app.api.services.app_service import AppService
from khalti.api.serializers.verify_serializers import VerifySerializer
from stripe_card.api.services.stripe_service import StripeService
from utils.helpers import dict_key_exists, get_client_ip


class CreatePaymentIntentView(generics.GenericAPIView):
    """Stripe Create Payment Intent Views

    Args:
        generics (GenericAPIView): GenericAPIView

    Returns:
        Response: Stripe Payment Intent Response
    """
    authentication_classes = [IsAuthenticatedApp]
    throttle_classes = [UserRateThrottle]
    serializer_class = VerifySerializer

    service = None

    def __init__(self) -> None:
        super().__init__()
        self.service = StripeService()

    def post(self, request):
        """Create Stripe Payment Intent

        Args:
            request : django request object
        """

        credential = AppService.get_credential(
            request.app, 'stripe',
            request.GET.get('credential_type'),
            request.GET.get('environment'))

        intent = self.service.create_payment_intent(
            credential,
            request.GET['amount'],
            request.GET['currency'],
            request.GET['email'])

        log = self.service.create_transaction_log(
            request.app,
            request.GET['credential_type'],
            request.GET['environment'],
            request.GET['amount'],
            request.GET['currency'],
            request.GET['customer'] if dict_key_exists(
                'customer', request.GET) else None,
            request.GET['reference_id'],
            get_client_ip(request),
            request.META['HTTP_USER_AGENT'],
            request.GET['remarks'],
            request.GET,
            intent
        )

        if not intent:
            return Response({
                'status': False,
                'message': self.service.getErrorMessage()
            }, self.service.getErrorCode())

        return Response({
            'status': True,
            'data': intent.id
        }, 200)
