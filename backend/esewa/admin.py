from django.contrib import admin
from esewa.models import EsewaTransaction,EsewaCredential
# Register your models here.
class EsewaTransactionAdmin(admin.ModelAdmin):
    list_display=[field.name for field in EsewaTransaction._meta.get_fields()]
    exclude = ['meta_data']

class EsewaCredentialAdmin(admin.ModelAdmin):
    list_display=[field.name for field in EsewaCredential._meta.get_fields()]
    

admin.site.register(EsewaTransaction,EsewaTransactionAdmin)
admin.site.register(EsewaCredential,EsewaCredentialAdmin)
