from typing import Any
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from awasam.orders.forms import NormalOrderForm
from awasam.orders.models import Normal, NormalOrderFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.


class ProfileLoginRequiredView(LoginRequiredMixin):
    def get_profile(self):
        return self.request.user.profile_user
# Create your views here.

class NormalOrderDetailView(ProfileLoginRequiredView, TemplateView):
    template_name = "dashboard/client/components/order/normal/detail.html"
    
    def get_order(self, **kwargs):
        return get_object_or_404(
            Normal,
            pk=kwargs["pk"],
            client=self.get_profile(),
            slug=kwargs.get("normal_order_slug")
        )
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["order"] = self.get_order(**kwargs)
        return context
    def post(self, *args, **kwargs):
        order = self.get_order(**kwargs)
        intent = self.request.POST.get("intent")
        if intent == 'instructions':
            order.revision_instruction = self.request.POST.get('instructions')
            order.save()
            messages.success(self.request, "Your update successfully save")
            
        if intent == 'comment':
            order.comment = self.request.POST.get('comment')
            order.save()
            messages.success(self.request, "your comment update successfully saved")
        return redirect(order.get_client_order_absolute_url())


@login_required
@csrf_exempt
@require_POST
def delete(request:HttpRequest, *args, **kwargs):
    order = get_object_or_404(
            Normal,
            pk=kwargs["pk"],
            client=request.user.profile_user,
            slug=kwargs.get("normal_order_slug")
        )
    order.is_active=False
    order.save()
    return redirect(reverse('dashboard:clients:orders:orders_list_view'))

            
        
    
