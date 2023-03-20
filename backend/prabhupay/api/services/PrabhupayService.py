import requests
from datetime import datetime
from prabhupay.models import PrabhupayCredential, PrabhupayTransaction
from stripe_card.models import TransactionStatus
from utils.api_service import ApiService
from utils.helpers import dict_get_value


class PrabhupayService(ApiService):
    """
        Prabhupay Utility Class

        Extends (ApiService)
    """

    def verify_transaction(self, credential: PrabhupayCredential, reference_id: str):
        """ Verify Khalti Transaction

        Args:
            credential (PrabhupayCredential): App khalti's Credential
            reference_id (str): Unique id of transaction

        Returns:
            PrabhupayTransaction: Khalti transaction log
        """
        try:
            url = credential.base_url + "api/v2/payment/verify/"
            payload = {
                "token": reference_id,
                "amount": 1000
            }
            headers = {
                "Authorization": "Key " + credential.secret_key
            }
            return requests.post(url, payload, headers=headers)
        except Exception as e:
            return self.setError(e, 422)

    @classmethod
    def create_transaction_log(cls, app, credential_type, environment, amount, reference_id, product_details, request_ip, user_agent, remarks, request_data) -> PrabhupayTransaction:
        """Create Prabhupay Transaction Log

        Args:
            app (App):App Object
            credential_type (str): which credentail to choose from if  multiple available
            environment (str): payment live or test?
            amount (float): transaction amount
            reference_id (str): unique refernce_id of transaction
            request_ip (str): ip of request creator
            user_agent (str): user agent of request creator
            remarks (str): remarks for the transaction

        """
        return PrabhupayTransaction.objects.create(
            app=app,
            amount=amount,
            remarks=remarks,
            user_agent=user_agent,
            request_ip=request_ip,
            meta_data=request_data,
            reference_id=reference_id,
            transaction_date=datetime.now(),
            credential_type=credential_type,
            product_details=product_details,
            is_test=True if environment == "test" else False,
            customer_name=dict_get_value("name", request_data),
            transaction_status=TransactionStatus.INITIATED.value,
            customer_phone=dict_get_value("phone", request_data),
            customer_email=dict_get_value("email", request_data),
        )

    @classmethod
    def update_transaction_log(cls, log: PrabhupayTransaction, response, error=""):
        """Update Khalti Transaction Log

        Args:
            log (PrabhupayTransaction): log object
            response (Object): requests.Response object

        Returns:
            void: return nothing
        """
        if response:
            success = True if response.status_code == 200 else False
        else:
            success = False

        if success:
            log.message = response.state.name
            log.transaction_id = response.idx
            log.transaction_status = TransactionStatus.COMPLETED.value
        else:
            log.message = error
            log.transaction_status = TransactionStatus.FAILED.value

        log.customer_name = response.user.name if success else None
        log.customer_phone = response.user.mobile if success else None
        log.meta_data = response.json()
        log.save()

    @classmethod
    def initiate_transaction(cls, credential: PrabhupayCredential, amount, reference_id, product_details, remarks, return_url):
        """Initiate prabhupay payment

        Args:
            credential (PrabhupayCredential): app credential
            amount (int): total amount for payment
            reference_id (str): unique transaction id
            product_details (list): list of json objects
            remarks (str): remarks for the payment
            return_url (str): redirection url after payment
        """
        headers = {'Content-type': 'application/json'}
        body = {
            "totalAmount": amount,
            "invoiceNo": reference_id,
            "merchantId": credential.merchant_id,
            "password": credential.merchant_password,
            "product_details": product_details,
            "remarks": remarks,
            "returnUrl": return_url
        }
        return requests.post(
            credential.base_url + "/api/EPayment/Initiate", json=body, headers=headers).json()

    @classmethod
    def verify_payment(cls, credential: PrabhupayCredential, reference_id: str):
        """Verify web payment 

        Args:
            credential (PrabhupayCredential): Prabhupay Credential Object
            reference_id (str): Unique transaction reference id (invoiceNo)
        """
        try:
            headers = {'Content-type': 'application/json'}
            body = {
                "invoiceNo": reference_id,
                "merchantId": credential.merchant_id,
                "password": credential.merchant_password
            }
            return requests.post(
                credential.base_url + "/api/EPayment/CheckStatus", json=body, headers=headers).json()
        except Exception:
            return cls.setError("Could not send verification request to prabhupay", 422)
