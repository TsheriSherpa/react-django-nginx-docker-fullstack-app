from base64 import encode
from urllib import response
from utils.api_service import ApiService
from imepay.models import ImePayCredential
import base64
import requests
import json
from imepay.models import ImePayTransaction
from datetime import datetime
from utils.helpers import dict_get_value
from stripe_card.models import TransactionStatus


class ImePayService(ApiService):
    """
    Esewa utility class

    Extends (ApiService)
    """

    def fetch_payment_token(request, credential: ImePayCredential):
        """

        """
        try:
            url = credential.base_url+"api/Web/GetToken"
            module = (credential.module).encode("ascii")
            token = (credential.api_username + ":" +
                     credential.password).encode('ascii')
            data = {
                'MerchantCode': credential.merchant_code,
                'RefId': request.data['reference_id'],
                'Amount': request.data['amount']
            }
            headers = {
                'Authorization': 'Basic ' + base64.b64encode(token).decode(),
                'Module': base64.b64encode(module).decode(),
                'Content-Type': 'application/json'
            }
            res = requests.post(url, data=json.dumps(data), headers=headers)
            return json.loads(res.text)
        except Exception as e:
            return super().set_error("Unable to fetch payload", 422)

    @classmethod
    def generate_payload(cls, token, credential, data):
        """Generate payload for topup transaction

        Args:
            token {dict}
            amount {float}
        Returns:
            payload {str}
        """
        callback_url = data['success_url']
        cancel_url = callback_url
        payload = (token['TokenId']+'|'+credential.merchant_code+'|'
                   + token['RefId']+'|'+data['amount']+'|'+'GET'
                   + '|'+callback_url+'|'+cancel_url
                   ).encode('ascii')

        return base64.b64encode(payload).decode()

    @classmethod
    def create_transaction_log(cls, token, app, credential_type, environment, amount, reference_id, request_ip, user_agent, remarks, request_data):
        return ImePayTransaction.objects.create(
            app=app,
            token=token,
            amount=amount,
            meta_data={},
            remarks=remarks,
            user_agent=user_agent,
            request_ip=request_ip,
            reference_id=reference_id,
            transaction_date=datetime.now(),
            credential_type=credential_type,
            is_test=True if environment == "test" else False,
            customer_name=dict_get_value("name", request_data),
            transaction_status=TransactionStatus.INITIATED.value,
            customer_phone=dict_get_value("phone", request_data),
            customer_email=dict_get_value("email", request_data),

        )

    @classmethod
    def update_transaction_log(cls, log: ImePayTransaction, response):

        if response[0] == "0":
            success = True
        else:
            success = False

        if success:
            log.customer_phone = response[2]
            log.transaction_id = response[3]
            log.transaction_status = TransactionStatus.COMPLETED.value
        else:
            log.customer_phone = response[2]
            log.transaction_status = TransactionStatus.FAILED.value

        log.message = response[1]

        log.save()

    @classmethod
    def web_callback(cls, enc_data):
        data = base64.b64decode(enc_data).decode()
        response = data.split('|')
        return response

    @classmethod
    def verify_payment(cls, credential: ImePayCredential, reference_id):
        try:
            reference_id = ImePayTransaction.objects.filter(reference_id=reference_id).first()
            headers = {
                'Authorization': 'Basic ' + base64.b64encode((credential.password).encode("ascii")).decode(),
                'Module': base64.b64encode((credential.module).encode("ascii")).decode(),
                'Content-Type': 'application/json'
            }
            payload = {
                "MerchantCode": credential.merchant_code,
                "RefId": reference_id.reference_id,
                "TokenId": reference_id.token,
                "TransactionId":reference_id.transaction_id,
                "Msisdn": reference_id.customer_phone
            }
            return requests.post(url=credential.base_url + "api/Web/Confirm",data=payload, headers=headers)
        except Exception as e:
            return cls.setError("Could not send verification request to imeay", 422)
