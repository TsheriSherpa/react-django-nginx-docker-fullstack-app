from datetime import datetime
import stripe
from utils.api_service import ApiService
from stripe_card.models import StripeCredential, StripeTransaction, TransactionStatus
from utils.helpers import dict_get_value


class StripeService(ApiService):
    """Stripe Service Class

    Extends:
        ApiService (Class): Extends ApiService Class
    """

    @classmethod
    def create_transaction_log(cls, app, credential_type, environment, amount, charge_currency, customer, reference_id, request_ip, user_agent, remarks, meta_data, payment_intent=None):
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

        Returns:
            StripeTransaction: StripeTransaction Object
        """
        return StripeTransaction.objects.create(
            app=app,
            amount=amount,
            remarks=remarks,
            customer=customer,
            meta_data=meta_data,
            user_agent=user_agent,
            request_ip=request_ip,
            currency=charge_currency,
            reference_id=reference_id,
            payment_intent=payment_intent,
            transaction_date=datetime.now(),
            credential_type=credential_type.upper(),
            customer_name=dict_get_value("name", meta_data),
            customer_phone=dict_get_value("phone", meta_data),
            customer_email=dict_get_value("email", meta_data),
            transaction_status=TransactionStatus.INITIATED.value,
            is_test=True if environment.upper() == "TEST" else False
        )

    def create_charge(self, amount, currency, customer, email, name, token, credential, description):
        """Create Stripe Charge

        Args:
            amount (float): Transaction Amount
            currency (str): Currency Symbol
            credential_type (str): Type Of Credential
            environment (str): is TEST or LIVE?
            customer (str): Stripe Customer ID
            email (str): Payment Initiator Email
            name (str): Payment Initiator Name
            token (str): Stripe Sdk Generated Token
            credential (StripeCredential): Stripe Credential Object
        """
        stripe.api_key = credential.secret_key
        if not customer:
            customer = self.create_stripe_customer(
                stripe, email, name, token, description)

        try:
            return stripe.Charge.create(
                amount=amount,
                currency=currency,
                customer=customer,
                receipt_email=email)

        except stripe.error.CardError as e:
            return self.setError("A payment error occurred: {}".format(e.user_message), 422)
        except stripe.error.InvalidRequestError:
            return self.setError("An invalid request occurred.", 422)
        except Exception as e:
            return self.setError("Something went wrong", 500)

    def create_stripe_customer(self, stripe, email, name, token, description):
        """Create Stripe Customer

        Args:
            stripe (stripe): Stripe object
            email (stripe): Customer email
            name (stripe): Customer name
            token (stripe): Stripe Token
        """
        try:
            return stripe.Customer.create(
                name=name,
                email=email,
                source=token,
                description=description,
            )
        except stripe.error.CardError as e:
            return self.setError("A payment error occurred: {}".format(e.user_message), 422)
        except stripe.error.InvalidRequestError:
            return self.setError("An invalid request occurred.", 422)
        except Exception as e:
            return self.setError("Something went wrong", 500)

    @classmethod
    def update_transaction_log(cls, log, charge, error="") -> None:
        """Update Transaction Log

        Args:
            log (StripeTransaction): Stripe Transaction Object
            charge (dict): Stripe Charge Response
        """
        if not charge:
            log.message = error
            log.transaction_status = TransactionStatus.FAILED.value

        else:
            log.charge_object = charge
            log.message = charge.status
            log.transaction_status = TransactionStatus.SUCCESS.value if charge.status == "succeeded" else TransactionStatus.ERROR.value

        log.save()

    def create_payment_intent(self, credential, amount, currency, email):
        """Create Stripe Payment Intent

        Args:
            credential (str): StripeCredential
            amount (int): total amount to be paid
            currency (str): currency used for payment
            email (str): email of the customer
        """
        try:
            stripe.api_key = credential.secret_key
            return stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                receipt_email=email,
                payment_method_types=["card", "alipay", "wechat_pay"],
            )
        except stripe.error.InvalidRequestError:
            return self.setError("Invalid parameters provided")
        except stripe.error.AuthenticationError:
            return self.setError("Authentication with stripe failed")
        except stripe.error.APIConnectionError:
            return self.setError("Network communication with Stripe failed")
        except stripe.error.StripeError:
            return self.setError("Error in stripe")
        except Exception:
            return self.setError("Something went wrong", 422)

    def capture_payment_intent(self, credential: StripeCredential, payment_intent: str):
        """Capture payment intent

        Args:
            payment_intent (str): Stripe Payment Intent ID
        """
        try:
            stripe.api_key = credential.secret_key
            return stripe.PaymentIntent.capture(payment_intent)
        except stripe.error.InvalidRequestError:
            return self.setError("Invalid intent provided")
        except stripe.error.AuthenticationError:
            return self.setError("Authentication with stripe failed")
        except stripe.error.APIConnectionError:
            return self.setError("Network communication with Stripe failed")
        except stripe.error.StripeError:
            return self.setError("Error in stripe")
        except Exception:
            return self.setError("Something went wrong", 422)
