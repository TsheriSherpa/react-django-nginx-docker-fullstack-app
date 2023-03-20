from esewa.models import EsewaCredential
from fonepay.models import FonepayCredential
from imepay.models import ImePayCredential
from khalti.models import KhaltiCredential
from ncell.models import NcellCredential
from prabhupay.models import PrabhupayCredential
from stripe_card.models import StripeCredential


class AppService:
    """ App Utility Class """

    @classmethod
    def get_credential(cls, app, gateway, credential_type, environment):
        if gateway == 'khalti':
            return KhaltiCredential.objects.filter(
                app=app, credential_type=credential_type.upper(), environment=environment.upper()).first()

        if gateway == 'stripe':
            return StripeCredential.objects.filter(app=app, credential_type=credential_type.upper(), environment=environment.upper()).first()

        if gateway == 'esewa':
            return EsewaCredential.objects.filter(app=app, credential_type=credential_type.upper(), environment=environment.upper()).first()

        if gateway == 'imepay':
            return ImePayCredential.objects.filter(app=app, credential_type=credential_type.upper(), environment=environment.upper()).first()

        if gateway == 'prabhupay':
            return PrabhupayCredential.objects.filter(app=app, credential_type=credential_type.upper(), environment=environment.upper()).first()

        if gateway == 'fonepay':
            return FonepayCredential.objects.filter(app=app, credential_type=credential_type.upper(), environment=environment.upper()).first()

        if gateway == 'ncell':
            return NcellCredential.objects.filter(app=app, credential_type=credential_type.upper(), environment=environment.upper()).first()

        raise Exception("Unknown Payment Gateway")
