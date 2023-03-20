from django.contrib import admin
from prabhupay.models import PrabhupayTransaction, PrabhupayCredential


class PrabhupayTransactionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PrabhupayTransaction._meta.fields if field.name not in (
        'id',)]


class PrabhupayCredentialAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PrabhupayCredential._meta.fields if field.name not in (
        'id', 'app')]


admin.site.register(PrabhupayTransaction, PrabhupayTransactionAdmin)
admin.site.register(PrabhupayCredential, PrabhupayCredentialAdmin)
