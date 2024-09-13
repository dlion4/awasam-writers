from django.urls import path, include


from . import views

app_name = "dashboard"

urlpatterns = [
    path("writers/", include("awasam.writers.urls", namespace="writers")),
    path("editors/", include("awasam.editors.urls", namespace="editors")),
    path("clients/", include("awasam.clients.urls", namespace="clients")),
    path("super-admin/", include("awasam.admins.urls", namespace="admins")),
    path("payments/", include("awasam.payments.urls", namespace="payments")),
    
]
