from django.contrib import admin
from django.apps import apps
from momopay.models import CreditTransaction, Credit
models = apps.get_models()

# Register your models here.
class CreditTransactionDisplay(admin.ModelAdmin):
    list_display= ('credit', 'transacted_by', 'transaction_amount', 'balance_before', 'balance_after', 'transaction_type')
 
class CredtDisplay(admin.ModelAdmin):
    list_display=('user', 'current_balance', 'time_updated')


admin.site.register(CreditTransaction, CreditTransactionDisplay)
admin.site.register(Credit, CredtDisplay)

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass