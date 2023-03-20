from django.contrib import admin
from esewa.models import EsewaTransaction,EsewaCredential
from .models import ImePayTransaction,ImePayCredential
# Register your models here.
class ImePayTransactionAdmin(admin.ModelAdmin):
    list_display=[field.name for field in ImePayTransaction._meta.get_fields()]
    exclude = ['meta_data']

class ImePayCredentialAdmin(admin.ModelAdmin):

    list_display=[field.name for field in ImePayCredential._meta.get_fields()]
    

admin.site.register(ImePayTransaction,ImePayTransactionAdmin)
admin.site.register(ImePayCredential,ImePayCredentialAdmin)
