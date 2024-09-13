from datetime import timezone
import itertools
from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from awasam.orders.models import Normal, NormalOrderCompleted
from awasam.payments.models import Transaction
from django.contrib import messages


class ProfileLoginRequiredView(LoginRequiredMixin):
    def get_profile(self):
        if self.request.user.is_authenticated:
            return self.request.user.profile_user
        return redirect(reverse("users:login"))


# Create your views here.

class DashboardMixinView(ProfileLoginRequiredView, TemplateView):
    template_name = ""
    

    def get_transactions(self):
        return Transaction.objects.prefetch_related("client").filter(client=self.get_profile())
    
    def get_orders(self):
        return (
            list(
                itertools.chain(self.get_profile().course_orders.all(), self.get_profile().normal_orders.all())
            )
        )
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["transactions"] = self.get_transactions()
        context["orders"] = self.get_orders()
        context["orders_count"] = len(self.get_orders())
        context["profile"] = self.get_profile()
        return context
    

class HomeView(DashboardMixinView):
    template_name = "dashboard/writer/pages/home.html"
    
writer_home_view = HomeView.as_view()


class WriterOrdersListView(DashboardMixinView):
    template_name = "dashboard/writer/pages/orders.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        return context
    def post(self, request:HttpRequest, *args, **kwargs):
        order_id = request.POST.get("order_id")
        order = get_object_or_404(Normal, pk=order_id)
        order.is_completed = True
        order.completed_date = timezone.now()
        order.save()
        normal_completed = NormalOrderCompleted(
            writer=self.get_profile(),
            normal_order=order,
            file=request.FILES.get("file"),
            comment=request.POST.get("comment"),
        )
        order.save()
        normal_completed.save()
        return redirect(reverse("dashboard:writers:writer_orders_view"))
    
class WriterNormalOrderDetailView(DashboardMixinView):
    template_name = "dashboard/writer/pages/normal_order_detail.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["order"] = get_object_or_404(self.get_profile().normal_orders, pk=self.kwargs.get("pk"), slug=kwargs.get("normal_order_slug"))
        return context
    
class WriterCourseOrderDetailView(DashboardMixinView):
    template_name = "dashboard/writer/pages/course_order_detail.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["order"] = get_object_or_404(self.get_profile().course_orders, pk=self.kwargs.get("pk"), slug=kwargs.get("course_order_slug"))
        return context
    
from awasam.users.forms import ProfileUpdateForm
from awasam.dashboard.views import DashboardAccountView
from awasam.users.forms import PasswordUpdateForm


class WriterDashboardAccountView(DashboardAccountView, DashboardMixinView):
    template_name = "dashboard/writer/account/index.html"
    change_password_form = PasswordUpdateForm
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["change_password_form"] = self.change_password_form()
        return context
    

    

writer_dashboard_account = WriterDashboardAccountView.as_view()