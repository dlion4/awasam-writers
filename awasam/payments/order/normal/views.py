import json
from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from awasam.payments.models import NormalOrderPayment
from awasam.orders.models import Normal
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings

import stripe


stripe.api_key = settings.STRIPE_API_KEY

class ProfileLoginRequiredView(LoginRequiredMixin):
    def get_profile(self):
        return self.request.user.profile_user

class NormalOrderPaymentView(ProfileLoginRequiredView, TemplateView):
    template_name = "dashboard/client/payments/home.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["profile"] = self.get_profile()
        context["order"] = Normal.objects.prefetch_related("client").filter(
            Q(client=self.get_profile())&Q(is_paid=False),
        ).latest()
        return context
    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


    
client_normal_order_payment_view = NormalOrderPaymentView.as_view()




class NormalOrderPayment(ProfileLoginRequiredView, View):
    order_model = Normal
    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def get_order(self, **kwargs):
        return (
            self.order_model.objects.prefetch_related("client").filter(
                Q(client=self.get_profile())&Q(is_paid=False)).latest())
        
    def post(self, request:HttpRequest, *args, **kwargs):
        success_url = reverse("dashboard:payments:orders:payment_success")
        cancel_url = reverse("dashboard:payments:orders:payment_cancel")
        normal_order = self.get_order(**kwargs)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'{normal_order.topic}',
                        },
                        'unit_amount': int(normal_order.price*100),  # $20 in cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri(success_url),
            cancel_url=request.build_absolute_uri(cancel_url),
        )
        return JsonResponse({'id': checkout_session.id})
        


class StripeNormalOrderPaymentCheckoutView(NormalOrderPayment):
    pass
create_checkout_session = StripeNormalOrderPaymentCheckoutView.as_view()
        
class StripeNormalDetailOrderPaymentCheckout(NormalOrderPayment):
    def get_order(self, **kwargs):
        return get_object_or_404(self.order_model,pk=kwargs.get("pk"))
create_detail_checkout_session = StripeNormalDetailOrderPaymentCheckout.as_view()


class OrderPaymentSuccessfulView(ProfileLoginRequiredView, TemplateView):
    template_name = 'dashboard/client/payments/success.html'
    def get_order_item(self):
        return Normal.objects.prefetch_related("client").filter(
            Q(client=self.get_profile())&Q(is_paid=False),
        ).latest()
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["profile"] = self.get_profile()
        context["order"] = self.get_order_item()
        return context
    def get(self, request, *args, **kwargs):
        order_item = self.get_order_item()
        order_item.is_paid = True
        order_item.save()
        return super().get(request, *args, **kwargs)
    
payment_success = OrderPaymentSuccessfulView.as_view()

def payment_cancel(request):
    return render(request, 'dashboard/client/payments/cancel.html')




