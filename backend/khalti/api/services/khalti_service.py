import requests
from datetime import datetime
from khalti.models import KhaltiCredential, KhaltiTransaction
from stripe_card.models import TransactionStatus
from utils.api_service import ApiService
from utils.helpers import dict_get_value


class KhaltiService(ApiService):
    """
        Khalti Utility Class

        Extends (ApiService)
    """

    def verify_transaction(self, credential: KhaltiCredential, reference_id: str):
        """ Verify Khalti Transaction

        Args:
            credential (KhaltiCredential): App khalti's Credential
            reference_id (str): Unique id of transaction

        Returns:
            KhaltiTransaction: Khalti transaction log
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
    def create_transaction_log(cls, app, credential_type, environment, amount, reference_id, request_ip, user_agent, remarks, request_data):
        """Create Khalti Transaction Log

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
        return KhaltiTransaction.objects.create(
            app=app,
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

    @ classmethod
    def update_transaction_log(cls, log: KhaltiTransaction, response, error=""):
        """Update Khalti Transaction Log

        Args:
            log (KhaltiTransaction): log object
            response (Object): requests.Response object

        R?ns:
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
        log.save()
