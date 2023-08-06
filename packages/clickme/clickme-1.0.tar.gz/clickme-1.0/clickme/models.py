from django.db import models


class Transaction(models.Model):
    PROCESS = 0
    VERIFY = 1
    PAID = 2
    FAILED = 3

    STATUS = (
        (PROCESS, 'processing'),
        (VERIFY, 'verify'),
        (PAID, 'paid'),
        (FAILED, 'failed')
    )

    payment_id = models.CharField(max_length=255, blank=True, null=True)
    order_id = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    status = models.CharField(max_length=10, default=PROCESS, choices=STATUS)
    error_code = models.IntegerField(blank=True, null=True)
    error_note = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    pay_time = models.DateTimeField(auto_now=True)

    def create_transaction(self, error_code, error_note, status=PROCESS):
        Transaction.objects.create(
            error_code=error_code,
            error_note=error_note,
            status=status
        )

    def update_transaction(self, trans, status, error_code, error_note, payment_id=None, order_id=None, amount=None):
        trans.status = status
        trans.error_code = error_code
        trans.error_note = error_note
        trans.order_id = order_id
        trans.amount = amount
        trans.payment_id = payment_id
        trans.save()
