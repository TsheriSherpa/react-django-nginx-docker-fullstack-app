from django.contrib import admin

from fonepay.models import FonepayTransaction, FonepayCredential


class FonepayTransactionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FonepayTransaction._meta.fields if field.name not in (
        'id',)]


class FonepayCredentialAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FonepayCredential._meta.fields if field.name not in (
        'id', 'app')]


admin.site.register(FonepayTransaction, FonepayTransactionAdmin)
admin.site.register(FonepayCredential, FonepayCredentialAdmin)
