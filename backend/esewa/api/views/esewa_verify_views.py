from multiprocessing.sharedctypes import Value
from app.api.services.app_service import AppService
from esewa.api.serializers.esewa_verify_serializer import EsewaVerifySerializer
from esewa.api.services.esewa_service import EsewaService
from ...models import EsewaTransaction
from khalti.api.serializers.verify_serializers import VerifySerializer
from khalti.api.services.khalti_service import KhaltiService
from stripe_card.models import TransactionStatus

from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from app.api.permissions.authenticated_app import IsAuthenticatedApp
from utils.helpers import get_client_ip


class EsewaVerifyView(generics.GenericAPIView):
    """ View for verifying khalti's payment

    Args:
        generics (GenericAPIView): GenericAPIView

    Returns:
        Response: Whether payment is success or not
    """
    authentication_classes = [IsAuthenticatedApp]
    throttle_classes = [UserRateThrottle]
    serializer_class = EsewaVerifySerializer
    service = None

    def __init__(self) -> None:
        super().__init__()
        self.service = EsewaService()

    @swagger_auto_schema(
        request_body=EsewaVerifySerializer,
        responses={
            200: str({
                'status': True,
                'data': "Transaction verified"
            })
        }
    )
    def post(self, request):
        """Get List Of Payment Available For App

        Args:
            request (request): django request

        Returns:
            list:
        """

        credential = AppService.get_credential(
            request.app, 'esewa', request.data['credential_type'], request.data['environment'])

        reference_id = EsewaTransaction.objects.filter(
            reference_id=request.data['reference_id'])
        if reference_id.exists():
            response = self.service.verify_transaction(
                credential, request.data['reference_id'])
            if response.status_code == 200:
                reference_id.update(
                    app=request.app,
                    reference_id=request.data['reference_id'],
                    remarks=request.data['remarks'],
                    status_code="00",
                    transaction_status=TransactionStatus.COMPLETED.value,
                    meta_data=request.data
                )
            else:
                reference_id.update(
                    app=request.app,
                    reference_id=request.data['reference_id'],
                    remarks=request.data['remarks'],
                    status_code="01",
                    transaction_status=TransactionStatus.FAILED.value,
                    meta_data=request.data
                )

        else:
            log = self.service.create_transaction_log(
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
            response = self.service.verify_transaction(
                credential, request.data['reference_id'])
            reference_id.update(
                app=request.app,
                reference_id=request.data['reference_id'],
                remarks=request.data['remarks'],
                status_code="00",
                transaction_status=TransactionStatus.COMPLETED.value,
                meta_data=request.data
            )

        return Response({
            'status': True,
            'data': "Transaction verified"
        }, 200)
