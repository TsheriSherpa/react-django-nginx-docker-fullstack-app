import requests
from core import settings
from esewa.models import EsewaCredential, EsewaTransaction
from utils.api_service import ApiService
from stripe_card.models import TransactionStatus
from datetime import datetime
from utils.helpers import dict_get_value
from django.shortcuts import get_object_or_404, redirect, render


class EsewaService(ApiService):
    """
    Esewa utility class

    Extends (ApiService)
    """

    def payment_transaction(self, request, credential: EsewaCredential, data):
        """ Verify Esewa Transaction

        Args:
            credential (EsewaCredential): App esewa's Credential
            reference_id (str): Unique id of transaction

        Returns:
            EsewaCredential: Esewa transaction log
        """
        url = credential.base_url+"epay/main/"
        payload = {
            'amt': data['amount'],
            'pdc': 0,
            'psc': 0,
            'txAmt': 0,
            'tAmt': 100,
            'pid': data['reference_id'],
            'scd': credential.secret_key,
            'su': settings.BASE_URL + "api/v1/esewa/web/callback/success",
            'fu': settings.BASE_URL + "api/v1/esewa/web/callback/failure"+"?oid="+data['reference_id'],
            'url': url
        }
        return render(request, 'esewa/index.html', payload)

    @classmethod
    def create_transaction_log(cls, app, credential_type, environment, amount, reference_id, request_ip, user_agent, remarks, request_data):
        return EsewaTransaction.objects.create(
            app=app,
            amount=amount,
            meta_data=request_data,
            remarks=remarks,
            status_code="01",
            user_agent=user_agent,
            request_ip=request_ip,
            reference_id=reference_id,
            transaction_date=datetime.now(),
            credential_type=credential_type,
            transaction_status=TransactionStatus.INITIATED.value,
            transaction_id=reference_id,
            is_test=True if environment == "test" else False,
            customer_name=dict_get_value("name", request_data),
            customer_phone=dict_get_value("phone", request_data),
            customer_email=dict_get_value("email", request_data),
        )

    @classmethod
    def update_transaction_log(cls, log: EsewaCredential, response, refId, error=""):
    
        """Update Esewa Transaction Log

        Args:
            log (EsewaTransaction): log object
            response (Object): requests.Response object

        Returns:
            void: return nothing
        """
        success = True if response == "success" else False

        if success:
            log.message = "Success"
            log.transaction_status = TransactionStatus.COMPLETED.value
            log.transaction_id = refId
        else:
            log.message = "Failure"
            log.transaction_status = TransactionStatus.FAILED.value

        log.status_code = "00" if success else "01"
        log.save()

    
    @classmethod
    def verify_transaction(cls,credential:EsewaCredential,reference_id):
        """ Verify Esewa Transaction

        Args:
            credential (EsewaCredential): App Esewa's Credential
            reference_id (str): Unique id of transaction

        Returns:
            EsewaTransaction: Esewa transaction log
        """
        url=credential.base_url+"mobile/transaction?txnRefId="+reference_id

        header={
            "merchantId":credential.public_key,
            "merchantSecret":credential.secret_key
        }
        return requests.get(url,headers=header)


    # @classmethod
    # def mobile_update_transaction_log(cls,log:EsewaCredential,response,error=""):
    #     """Update Khalti Transaction Log

    #     Args:
    #         log (KhaltiTransaction): log object
    #         response (Object): requests.Response object

    #     Returns:
    #         void: return nothing
    #     """
    #     success = True if response.status_code == 200 else False

    #     if success:
    #         log.app=response.app
    #         log.message = response.state.name
    #         log.transaction_status = TransactionStatus.COMPLETED
    #         log.transaction_id = response.idx
    #     else:
    #         log.message = error
    #         log.transaction_status = TransactionStatus.FAILED

    #     log.status_code = "00" if success else "01"
    #     log.customer_name = response.user.name if success else None
    #     log.customer_phone = response.user.mobile if success else None
    #     log.meta_data = response.json()
    #     log.save()

    
        




