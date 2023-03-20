from django.http import HttpResponseRedirect
from django.shortcuts import render

from rest_framework import generics
from fonepay.models import FonepayTransaction
from stripe_card.models import TransactionStatus


class PaymentCallbackView(generics.GenericAPIView):
    """ Handle fonepay callback request

    Args:
        generics (GenericAPIView): GenericAPIView

    Returns:
        Response: Redirect to web view
    """
    service = None

    def __init__(self) -> None:
        super().__init__()

    def get(self, request):
        """ Fonepay return request handle

        Args:
            request (request): django request

        Returns:
            response: Django Template || Redirect 
        """
        log = FonepayTransaction.objects.filter(
            reference_id=request.GET['PRN']).first()

        log.message = request.GET['RC']
        log.transaction_id = request.GET['UID']

        if not request.GET['PS']:
            log.transaction_status = TransactionStatus.CANCELLED.value if request.GET[
                'RC'] == "cancel" else TransactionStatus.FAILED.value
        else:
            log.transaction_status = TransactionStatus.COMPLETED.value

        log.save()

        if log.meta_data['is_mobile']:
            return render(request, 'result.html', {'status': request.GET['RC']})

        return HttpResponseRedirect(log.meta_data['return_url'] + "?status=" + "success" if request.GET['PS'] else "failed")
