from django.contrib import admin
from esewa.models import EsewaTransaction, EsewaCredential
from .models import NcellTransaction, NcellCredential
# Register your models here.


class NcellTransactionAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in NcellTransaction._meta.get_fields()]
    exclude = ['meta_data']


class NcellCredentialAdmin(admin.ModelAdmin):

    list_display = [
        field.name for field in NcellCredential._meta.get_fields()]


admin.site.register(NcellTransaction, NcellTransactionAdmin)
admin.site.register(NcellCredential, NcellCredentialAdmin)
