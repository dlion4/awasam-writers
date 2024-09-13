from django.urls import path, include

from . import views

app_name = "dashboard:payments"

urlpatterns = [
    path("", include("awasam.payments.order.normal.urls", namespace="orders")),
    path("", views.PaymentListView.as_view(), name="payment_view"),
    path("action/deposit/", views.TopUpView.as_view(), name="top_up_action_view"),
    path("completed/", views.payment_success, name="payment_success"),
    path("cancelled/", views.payment_cancel, name="payment_cancel"),
    path("deposit/view/", views.TopUpWalletView.as_view(), name="top_up_view"),
    
    path("<paper_id>/", views.payment_for_paper,name="purchase_paper"),
]
