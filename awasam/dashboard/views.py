from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from awasam.payments.models import Transaction
from django.db.models import Sum


class ProfileLoginRequiredView(LoginRequiredMixin):
    def get_profile(self):
        return self.request.user.profile_user


# Create your views here.

class DashboardMixinView(ProfileLoginRequiredView, TemplateView):
    template_name = ""
    
    def get_transactions(self):
        return Transaction.objects.prefetch_related("client").filter(client=self.get_profile())
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_profile()
        context["orders"] = self.get_order_items()
        context["transaction_balance"] = self.get_transactions().aggregate(amount=Sum("amount"))["amount"]
        return context

from awasam.users.forms import ProfileUpdateForm
    
class DashboardAccountView:
    template_name = ""
    form_class = ProfileUpdateForm
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["profile_form"] = self.form_class(instance=self.get_profile())
        return context
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=self.get_profile())
        if form.is_valid():
            form.save()
            messages.success(request,"Your profile was updated successfully")
            return redirect(reverse("dashboard:writers:account"))
        messages.error(request, "Error updating your profile")
        return redirect("dashboard:writers:account")