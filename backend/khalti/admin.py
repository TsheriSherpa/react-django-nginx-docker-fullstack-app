from django.contrib import admin

from khalti.models import KhaltiTransaction, KhaltiCredential


class KhaltiTransactionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in KhaltiTransaction._meta.fields if field.name not in (
        'id',)]


class KhaltiCredentialAdmin(admin.ModelAdmin):
    list_display = [field.name for field in KhaltiCredential._meta.fields if field.name not in (
        'id', 'app')]


admin.site.register(KhaltiTransaction, KhaltiTransactionAdmin)
admin.site.register(KhaltiCredential, KhaltiCredentialAdmin)
