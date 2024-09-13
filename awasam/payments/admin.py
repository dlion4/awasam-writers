from django.contrib import admin

# Register your models here.
from .models import (
    NormalOrderPayment,
    Transaction
)

@admin.register(NormalOrderPayment)
class NormalOrderPaymentAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'amount',
        'payment_date',
        'payment_status',
    ]
    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'client',
        'amount',
        'payment_date',
    )
