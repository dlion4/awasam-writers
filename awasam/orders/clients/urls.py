from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.OrdersListView.as_view(), name="orders_list_view"),
]
