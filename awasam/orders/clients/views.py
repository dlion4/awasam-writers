from typing import Any
from django.views.generic import TemplateView
from awasam.orders.models import Normal
from awasam.orders.views import ProfileLoginRequiredView

class OrdersListView(ProfileLoginRequiredView, TemplateView):
    template_name = "dashboard/client/components/order/normal/list.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["orders"] = Normal.objects.prefetch_related("client").filter(client=self.get_profile()).filter(is_active=True)
        return context
    