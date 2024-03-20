from django.contrib import admin
from .models import Product, Order, Payment
import requests
import json
import time


class OrderAdmin(admin.ModelAdmin):
    actions = ['confirm_order']

    def confirm_order(self, request, queryset):
        for order in queryset:
            if order.payment.status == 'Paid':
                order.status = 'Confirmed'
                order.confirmation_time = timezone.now()
                order.save()

                # Имитация подготовки заказа
                time.sleep(5)

                payload = {
                    "id": order.id,
                    "amount": order.total_amount,
                    "date": order.confirmation_time.strftime("%Y-%m-%d %H:%M:%S")
                }
                requests.post('https://webhook.site/36693e00-8f59-4f7b-9a85-1d1e7ddde4d4', data=json.dumps(payload))

    confirm_order.short_description = "Confirm selected orders"


admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
