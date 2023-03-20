from lib2to3.pgen2 import token
from urllib import response
from imepay.api.services.imepay_service import ImePayService
from rest_framework import generics
from rest_framework.response import Response
from imepay.models import ImePayTransaction
import base64

from utils.api_response import ApiResponse

class ImePayWebCallback(generics.GenericAPIView):

    def __init__(self) -> None:
        super().__init__()

    def get(self, request):
        data = request.GET.get("data")
        response=ImePayService.web_callback(data)
        log=ImePayTransaction.objects.filter(token=response[6]).first()
        print("loggggggggggggggggggg",response[6])
        service=ImePayService()
        service.update_transaction_log(log,response)

        if response[0]=="0":
            return ApiResponse.send_success(response[1])
        else:
            return ApiResponse.send_error(response[1])
        
        
