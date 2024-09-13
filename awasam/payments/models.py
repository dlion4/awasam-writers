from django.db import models

# Create your models here.
class NormalOrderPayment(models.Model):
    order = models.ForeignKey('orders.Normal', on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1,
        choices=(
            ('S', 'Successful'),
            ('C', 'Cancelled'),
            ('F', 'Failed'),
        ),
        default='S',
    )
    
    
class Transaction(models.Model):
    client = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="profile_transactions")
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    payment_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True)
    type = models.CharField(max_length=1, choices=(("D", "Debit"), ("C", "Credit")), default="D")
    
    def __str__(self):
        return f"Payment: {self.reason}"