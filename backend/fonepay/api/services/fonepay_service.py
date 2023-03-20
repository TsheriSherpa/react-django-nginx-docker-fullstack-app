""" Fonepay  Utility Class """

import hmac
import hashlib
from urllib.parse import urlencode
from datetime import datetime

from django.conf import settings

from utils.helpers import dict_get_value
from utils.api_service import ApiService
from stripe_card.models import TransactionStatus
from fonepay.models import FonepayCredential, FonepayTransaction


class FonepayService(ApiService):

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
        return FonepayTransaction.objects.create(
            app=app,
            amount=amount,
            remarks=remarks,
            user_agent=user_agent,
            request_ip=request_ip,
            meta_data=request_data,
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
    def initiate_payment(cls, credential: FonepayCredential, log: FonepayTransaction):
        """Initiate fonepay payment

        Args:
            credential (FonepayCredential): FonepayCredential Object
            log (FonepayTransaction): FonepayTransaction Object
        """
        params = cls.prepare_payment_params(credential, log)
        params = urlencode(params)

        return credential.base_url + '/api/merchantRequest?' + params

    @classmethod
    def prepare_payment_params(cls, credential: FonepayCredential, log: FonepayTransaction):
        """Prepare request params for fonepay payment initiate request

        Args:
            credential (FonepayCredential): FonepayCredential Object
            log (FonepayTransaction): FonepayTransaction Object
        Returns:
            params (dict): prepared params dict
        """
        return_url = settings.BASE_URL + '/api/v1/fonepay/payment/callback'
        dv = cls.create_secure_hash(
            credential.secret_key,
            credential.merchant_code,
            "P", log.reference_id,
            log.amount, "NPR",
            datetime.now().strftime("%d/%m/%Y"),
            log.remarks, "NA", return_url
        )

        return {
            "DV": dv,
            "MD": "P",
            "R2": "N/A",
            "CRN": "NPR",
            "RU": return_url,
            "AMT": log.amount,
            "R1": log.remarks,
            "PRN": log.reference_id,
            "PID": credential.merchant_code,
            "DT": datetime.now().strftime("%d/%m/%Y")
        }

    @classmethod
    def create_secure_hash(cls, secret_key, pid, md, prn, amt, crn, dt, r1, r2, ru):
        """Create secure hash using HMAC_SHA512

        Args:
            pid (str): merchant_code
            md (str): P for payment
            prn (str): product reference number
            amt (double): payable amount
            crn (str): currency max 3 length
            dt (str): date format(dd/mm/yyyy)
            r1 (str): remarks 1
            r2 (str): remarks 2
            ru (str): return url

        Returns:
            hash (str): HMAC_SHA512
        """
        payload = [pid, md, prn, amt, crn, dt, r1, r2, ru]
        paybytes = ",".join(payload).encode('utf8')
        return hmac.new(secret_key.encode('utf8'), paybytes, hashlib.sha512).hexdigest()
