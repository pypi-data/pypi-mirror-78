from django.contrib import admin
from clickme.models import Transaction


class TransactionModelAdmin(admin.ModelAdmin):

    def get_status(self, obj):
        return obj.get_status_display()
    get_status.short_description = 'status'

    search_fields = ('order_id',)
    list_display = ['payment_id', 'order_id', 'amount', 'get_status', 'create_time', 'pay_time']


admin.site.register(Transaction, TransactionModelAdmin)
