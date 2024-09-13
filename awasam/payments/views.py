import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from awasam.clients.views import ProfileLoginRequiredView
from django.conf import settings
from django.db.models import Q
from typing import Any
import stripe
import contextlib

from awasam.orders.models import NormalOrderCompleted
from awasam.payments.models import Transaction


stripe.api_key = settings.STRIPE_API_KEY

# Create your views here.
class PaymentListView(ProfileLoginRequiredView, TemplateView):
    template_name = "dashboard/payments/index.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["transactions"] = Transaction.objects.prefetch_related("client").filter(client=self.get_profile())
        return context
    

class TopUpWalletView(ProfileLoginRequiredView, TemplateView):
    template_name = "dashboard/payments/add_fund.html"
    
class TopUpView(ProfileLoginRequiredView, View):
    def post(self, request:HttpRequest, *args, **kwargs):
        success_url = reverse("dashboard:payments:payment_success")
        cancel_url = reverse("dashboard:payments:payment_cancel")
        try:
            amount = int(json.loads(request.body).get("amount"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid amount format"}, status=400)
        
        Transaction.objects.create(
            client=self.get_profile(),
            amount=amount,
            reason="Acount Top Up"
        )

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'{self.get_profile().user.email}: Account TopUp',
                        },
                        'unit_amount': int(amount*100),  # 2000 = $20 in cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri(success_url),
            cancel_url=request.build_absolute_uri(cancel_url),
        )
        return JsonResponse({
            'id': checkout_session.id
        })
        
def payment_cancel(request):
    return render(request, 'dashboard/payments/cancel.html')


# Transaction
class TopUpPaymentSuccessfulView(ProfileLoginRequiredView, TemplateView):
    template_name = 'dashboard/payments/success.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["transactions"] = Transaction.objects.prefetch_related("client").filter(client=self.get_profile())
        return context
    
payment_success = TopUpPaymentSuccessfulView.as_view()

class PurchasePaperView(View):
    def post(self, request:HttpRequest, *args, **kwargs):
        try:
            data:dict = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid data format"}, status=400)
        paper = NormalOrderCompleted.objects.get(pk=kwargs.get("paper_id"))
        email_address = data.get("email_address")
        
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items = [
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'{paper.normal_order.assignment_type_text}',
                            'description': (
                                f'Academic Level: {paper.normal_order.get_academic_level_display()}\n'
                                f'Discipline: {paper.normal_order.get_subject_display()}\n'
                                f'Paper Format: {paper.normal_order.get_citation_display()}\n'
                                f'Sources: {paper.normal_order.get_sources_display()}'
                            ),  # Add detailed description here
                        },
                        'unit_amount': int(int(paper.normal_order.price * 100) / 2),  # e.g., $20 in cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri(reverse("sample_orders")),
            cancel_url=request.build_absolute_uri(reverse("sample_orders")),
        )
        return JsonResponse({
            'id': checkout_session.id
        })
payment_for_paper  = PurchasePaperView.as_view()