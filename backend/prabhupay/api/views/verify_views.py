from rest_framework import generics
from rest_framework.throttling import UserRateThrottle

from drf_yasg.utils import swagger_auto_schema

from app.api.permissions.authenticated_app import IsAuthenticatedApp
from app.api.services.app_service import AppService
from prabhupay.api.serializers.payment_verify_serializers import PaymentVerifySerializer
from prabhupay.api.services.PrabhupayService import PrabhupayService
from prabhupay.models import PrabhupayTransaction
from stripe_card.models import TransactionStatus
from utils.api_response import ApiResponse
from utils.helpers import get_error_message


class PaymentVerifyView(generics.GenericAPIView):
    """ Make Payment From Prabhupay 

    Args:
        generics (GenericAPIView): GenericAPIView

    Returns:
        Response: Access Token
    """
    service = None
    throttle_classes = [UserRateThrottle]
    serializer_class = PaymentVerifySerializer
    authentication_classes = [IsAuthenticatedApp]

    def __init__(self):
        super().__init__()

    @swagger_auto_schema(
        request_body=PaymentVerifySerializer,
        responses={
            200: str({
                "status": True,
                "data": {
                    "status": "00",
                    "success": True,
                    "message": "Operation Success",
                    "data": {
                        "amount": 100.0,
                        "charge": 0.0,
                        "invoiceNo": "sdsxfsedf",
                        "transactionId": "223408220644150604"
                    },
                    "note": None
                }
            })
        }
    )
    def post(self, request):
        """Make payment from prabhupay

        Args:
            request (request): django request

        Returns:
            dict:
        """

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.send_error(get_error_message(serializer), 400)

        credential = AppService.get_credential(
            request.app, 'prabhupay', request.data['credential_type'], request.data['environment'])

        response = PrabhupayService.verify_payment(
            credential,
            request.data.get('reference_id'),
        )

        if not response:
            return ApiResponse.send_error(
                PrabhupayService.getErrorMessage(),
                PrabhupayService.getErrorCode())

        log = PrabhupayTransaction.objects.filter(
            reference_id=request.data.get('reference_id')).first()

        if response['status'] == "00":
            log.message = response['message']
            log.transaction_id = response['data']['transactionId']
            log.transaction_status = TransactionStatus.COMPLETED.value
            log.save()
            return ApiResponse.send_success(response)

        log.transaction_status = TransactionStatus.FAILED.value
        log.message = response['message']
        log.save()

        return ApiResponse.send_error(response['message'])
