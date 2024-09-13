from django.urls import path, include
from . import views

app_name = "dashboard:clients:orders"

urlpatterns = [
    path("normal/<pk>/<normal_order_slug>/", views.NormalOrderDetailView.as_view(), name="normal_order_detail_view"),
    path("normal/<pk>/<normal_order_slug>/delete/", views.delete, name="normal_order_delete_view"),
    path("", include("awasam.orders.clients.urls")),
]
