from django.urls import path
from . import views

app_name = "dashboard:payments:orders"

urlpatterns = [
    path("normal-order-payment", views.client_normal_order_payment_view, name="normal_order_payment_view"),
  
    path('payment/stripe/', views.create_checkout_session, name='create_checkout_session'),
    path('payment/stripe/<pk>/', views.create_detail_checkout_session, name='create_detail_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
]
