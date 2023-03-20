from rest_framework import generics
from app.api.permissions.authenticated_app import IsAuthenticatedApp
from rest_framework.throttling import UserRateThrottle
from imepay.api.services.imepay_service import ImePayService
from utils.helpers import get_client_ip
from app.api.services.app_service import AppService
from rest_framework.response import Response
from imepay.api.serializers.imepay_payment_serializers import WebPaymentSerializer
from utils.api_response import ApiResponse
from utils.helpers import get_client_ip, get_error_message


class ImepayPaymentView(generics.GenericAPIView):
    """ View for payment payhment

    Args:
        generics (GenericAPIView): GenericAPIView

    Returns:
        Response: Whether payment is success or not
    """
    authentication_classes=[IsAuthenticatedApp]
    throttle_classes=[UserRateThrottle]
    serializer_class = WebPaymentSerializer
    

    service=None
    def __init__(self) -> None:
        super().__init__()
        self.service=ImePayService

    def post(self,request):
        serializer=self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return ApiResponse.send_error(get_error_message(serializer), 400)

        credential=AppService.get_credential(request.app,'imepay',request.data['credential_type'],request.data['environment'])
        token=ImePayService.fetch_payment_token(request,credential)
        log=ImePayService.create_transaction_log(
            token['TokenId'],
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
        payload=ImePayService.generate_payload(token,credential,request.data)
        return Response({
            "status":True,
            "url":credential.base_url+"WebCheckout/Checkout?data="+str(payload),
        })
        