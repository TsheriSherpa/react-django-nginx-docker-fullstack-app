from rest_framework import generics
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from app.api.permissions.authenticated_app import IsAuthenticatedApp
from app.api.services.app_service import AppService
from khalti.api.serializers.verify_serializers import VerifySerializer
from stripe_card.api.services.stripe_service import StripeService
from stripe_card.models import StripeTransaction


class VerifyPaymentIntentView(generics.GenericAPIView):
    """Verify Charge Using Payment Intent

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
        """Check if payment is success using payment_intent

        Args:
            request : django request object
        """
        log = StripeTransaction.objects.filter(
            reference_id=request.GET['reference_id']).first()

        if not log:
            return Response({
                'status': False,
                'message': "Unknown reference_id"
            }, 400)

        credential = AppService.get_credential(
            request.app,
            'stripe',
            log.credential_type,
            "TEST" if log.is_test == 1 else "LIVE")

        intent = self.service.capture_payment_intent(
            credential, request.GET['reference_id'])

        charge = intent.charges.data[0] if intent else None

        self.service.update_transaction_log(
            log, charge, self.service.getErrorMessage())

        if not intent:
            return Response({
                'status': False,
                'message': self.service.getErrorMessage()
            }, self.service.getErrorCode())

        return Response({
            'status': True,
            'data': "Payment Successfull"
        }, 200)
