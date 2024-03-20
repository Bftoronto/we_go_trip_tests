from django.urls import path
from .views import get_product_list, create_order, create_payment

urlpatterns = [
    path('products/', get_product_list, name='product-list'),
    path('order/', create_order, name='create-order'),
    path('payment/', create_payment, name='create-payment'),
]