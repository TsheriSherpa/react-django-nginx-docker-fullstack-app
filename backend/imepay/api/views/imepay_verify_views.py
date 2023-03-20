from rest_framework import generics
from rest_framework.throttling import UserRateThrottle

from drf_yasg.utils import swagger_auto_schema

from app.api.permissions.authenticated_app import IsAuthenticatedApp
from app.api.services.app_service import AppService
from imepay.api.serializers.verify_serializer import PaymentVerifySerializer
from stripe_card.models import TransactionStatus
from utils.api_response import ApiResponse
from utils.helpers import get_error_message
from imepay.api.services.imepay_service import ImePayService
from imepay.models import ImePayTransaction

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

    def post(self, request):
        

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.send_error(get_error_message(serializer), 400)

        credential = AppService.get_credential(request.app, 'imepay', request.data['credential_type'], request.data['environment'])
        response = ImePayService.verify_payment(
            credential,
            request.data['reference_id'],
        )
        log=ImePayTransaction.objects.filter(reference_id=request.data['reference_id']).first()

        if response['ResponseCode']=="0":
            log.message = response['ResponseDescription']
            log.transaction_id = response['TransactionId']
            log.transaction_status = TransactionStatus.COMPLETED.value
            log.save()
            return ApiResponse.send_success(response)

        log.transaction_status = TransactionStatus.FAILED.value
        log.message = response['ResponseDescription']
        log.save()

        return ApiResponse.send_error(response['ResponseDescription'])
