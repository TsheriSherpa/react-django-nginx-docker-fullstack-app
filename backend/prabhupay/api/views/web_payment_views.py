from rest_framework import generics
from rest_framework.throttling import UserRateThrottle

from drf_yasg.utils import swagger_auto_schema

from app.api.permissions.authenticated_app import IsAuthenticatedApp
from app.api.services.app_service import AppService
from prabhupay.api.serializers.web_payment_serializers import WebPaymentSerializer
from prabhupay.api.services.PrabhupayService import PrabhupayService
from utils.api_response import ApiResponse
from utils.helpers import get_client_ip, get_error_message


class WebPaymentView(generics.GenericAPIView):
    """ Make Payment From Prabhupay Through Web Channel

    Args:
        generics (GenericAPIView): GenericAPIView

    Returns:
        Response: Access Token
    """
    service = None
    throttle_classes = [UserRateThrottle]
    serializer_class = WebPaymentSerializer
    authentication_classes = [IsAuthenticatedApp]

    def __init__(self):
        super().__init__()
        self.service = PrabhupayService()

    @swagger_auto_schema(
        request_body=WebPaymentSerializer,
        responses={
            200: str({
                "status": True,
                "data": {
                    "status": "00",
                    "success": True,
                    "message": "Successful Operation",
                    "data": {
                        "redirectionUrl": "https://stageepayment.prabhupay.com/?processId=fa8c5d8b-690a-4553-883d-9de6b503d85e",
                        "processId": "fa8c5d8b-690a-4553-883d-9de6b503d85e"
                    },
                    "transactionId": "223408220603150601"
                }
            })
        }
    )
    def post(self, request):
        """Make payment from prabhupay web channel

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

        log = self.service.create_transaction_log(
            request.app,
            request.data.get('credential_type'),
            request.data.get('environment'),
            request.data.get('amount'),
            request.data.get('reference_id'),
            request.data.get('product_details'),
            get_client_ip(request),
            request.META['HTTP_USER_AGENT'],
            request.data.get('remarks'),
            request.data
        )

        response = self.service.initiate_transaction(
            credential,
            log.amount,
            log.reference_id,
            log.product_details,
            log.remarks,
            request.data.get("return_url")
        )

        if response['status'] == "00":
            return ApiResponse.send_success(response)

        return ApiResponse.send_success(response['message'])
