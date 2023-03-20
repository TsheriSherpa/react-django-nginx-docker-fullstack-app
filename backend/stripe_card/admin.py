from django.contrib import admin

from stripe_card.models import StripeTransaction
from stripe_card.models import StripeCredential


class StripeTransactionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in StripeTransaction._meta.fields if field.name not in (
        'id',)]


class StripeCredentialAdmin(admin.ModelAdmin):
    list_display = [field.name for field in StripeCredential._meta.fields if field.name not in (
        'id', 'app')]


admin.site.register(StripeTransaction, StripeTransactionAdmin)
admin.site.register(StripeCredential, StripeCredentialAdmin)
