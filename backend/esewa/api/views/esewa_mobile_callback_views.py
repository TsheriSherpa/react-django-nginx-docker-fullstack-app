from rest_framework import generics
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from esewa.api.serializers.esewa_web_callback_serializers import EsewaWebCallbackSerializer
from utils.helpers import get_client_ip

from ...models import EsewaTransaction
from esewa.api.services.esewa_service import EsewaService


class EsewaMobileCallback(generics.GenericAPIView):
    service = None
    serializer_class = EsewaWebCallbackSerializer

    def __init__(self) -> None:
        super().__init__()
        self.service = EsewaService()

    @swagger_auto_schema(request_body=None, responses=None)
    def post(self, request):
        if EsewaTransaction.objects.filter(reference_id=request.data['transactionDetails']['referenceId']).exists():
            return Response({
                "status": False,
                "message": "Reference aready used"
            }, 422)
        else:
            self.service.create_transaction_log(
                request.data['app'] if 'app' in request.data else None,
                request.data['credential_type'] if 'credential_type' in request.data else '',
                request.data['environment'] if 'environment' in request.data else '',
                request.data['totalAmount'],
                request.data['transactionDetails']['referenceId'],
                get_client_ip(request),
                request.META['HTTP_USER_AGENT'],
                request.data['remarks'] if 'remarks' in request.data else '',
                request.data
            )

        return Response({
            "status": True if request.data['transactionDetails']['status'] == "COMPLETE" else False,
            "message": request.data['message']['technicalSuccessMessage']
        })
