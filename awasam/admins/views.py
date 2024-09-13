import itertools
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from awasam.clients.views import ProfileLoginRequiredView
from typing import Any
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from awasam.orders.forms import NormalOrderForm
from awasam.orders.models import Course, Normal, NormalOrderCompleted, NormalOrderFile
from django.contrib.auth.mixins import LoginRequiredMixin
from awasam.payments.models import Transaction
from django.db.models import Sum

from urllib.parse import unquote
from typing import Any
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from awasam.payments.models import Transaction
from django.db.models import Sum

from awasam.users.models import Profile, User
from django.http import HttpResponse
from django.conf import settings
import os


class ProfileLoginRequiredView(LoginRequiredMixin):
    def get_profile(self):
        return self.request.user.profile_user


# Create your views here.

class DashboardMixinView(ProfileLoginRequiredView, TemplateView):
    template_name = ""
    
    def get_transactions(self):
        return Transaction.objects.prefetch_related("client").filter(client=self.get_profile())
    
    def get_order_items(self):
        courses = Course.objects.select_related('client').all()
        normal_orders = Normal.objects.select_related('client').all()
        return list(itertools.chain(courses, normal_orders))
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_profile()
        context["orders"] = self.get_order_items()
        context["courses"] = Course.objects.prefetch_related("client").all()
        context["orders_count"] = len(self.get_order_items())
        context["transaction_balance"] = self.get_transactions().aggregate(amount=Sum("amount"))["amount"]
        return context

# Create your views here.
class HomeView(DashboardMixinView):
    template_name = "dashboard/admins/pages/home.html"
admin_home_view = HomeView.as_view()

from django import forms

class AssignOrderForm(forms.Form):
    writers = forms.ModelChoiceField(
        queryset=User.objects.filter(account_type="Writer"),
        widget=forms.Select(attrs={
            "class": "form-control",
            "data-placeholder": "Select a Writer",
        })
    )
    order_type = forms.CharField(widget=forms.HiddenInput())
    order_pk = forms.CharField(widget=forms.HiddenInput())


class AdminOrdersListView(DashboardMixinView):
    template_name = "dashboard/admins/pages/orders.html"
    assign_order_form = AssignOrderForm
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["assign_order_form"] = self.assign_order_form()
        return context
    def post(self, request, *args, **kwargs):
        form = self.assign_order_form(request.POST)
        status = request.POST.get("status", None)
        if form.is_valid():
            writer = form.cleaned_data.get("writers", None)
            order_type = form.cleaned_data.get("order_type")
            order_pk = form.cleaned_data.get("order_pk")
            
            
            profile_writer = Profile.objects.get(user=writer)
            
            if order_type == "C" and writer:
                order = Course.objects.get(pk=order_pk)
                profile_writer.course_orders.add(order)
                order.is_assigned=True
                order.save()
                if status:
                    if status == "3":
                        order.is_completed = True
                        order.save()
                profile_writer.save()
                return redirect(reverse("dashboard:admins:admin_courses_view"))
            
            if order_type == "N":
                order = Normal.objects.get(pk=order_pk)
                profile_writer.normal_orders.add(order)
                order.is_assigned=True
                order.save()
                profile_writer.save()
                return redirect(reverse("dashboard:admins:admin_orders_view"))
        return redirect(reverse("dashboard:admins:admin_orders_view"))



admin_orders_view = AdminOrdersListView.as_view()

# class AdminApproveOrderView(DashboardMixinView):
def serve_file(request, pk, file_type, file_name):
    # Decode the file name from URL encoding
    
    # Fetch the file object
    normal_order_completed = get_object_or_404(NormalOrderCompleted, normal_order__pk=pk)
    file = normal_order_completed.file
    
    # Determine the content type based on file_type or filename
    content_type = 'application/octet-stream'  # Default MIME type
    if file_type == 'application/msword':
        content_type = 'application/msword'
    elif file_type == 'text/plain':
        content_type = 'text/plain'
    elif hasattr(file, 'content_type'):
        content_type = file.content_type
    
    # Construct the file path
    file_path = file.path
    
    # Check if the file exists
    if not os.path.exists(file_path):
        return HttpResponse("File not found", status=404)
    
    # Open and read the file
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)
        response['Content-Disposition'] = 'inline; filename="{}"'.format(file)
        return response

    # def get(self, request, pk, file_type, file_name):
    #     return self.serve_file(request, pk, file_type, file_name)

# admin_approve_order_view = AdminApproveOrderView.as_view()/



class AssignOrderForm(forms.Form):
    writers = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.filter(account_type="Writer"),
        widget=forms.Select(attrs={
            "class": "form-control",
            "data-placeholder": "Select a Writer",
        })
    )
    order_pk = forms.CharField(widget=forms.HiddenInput())

class AdminCoursesListView(DashboardMixinView):
    template_name = "dashboard/admins/pages/courses.html"
    assign_order_form = AssignOrderForm
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["assign_order_form"] = self.assign_order_form()
        return context
    


def admin_orders_mark_approved_view(request, pk, normal_order_slug):
    normal_order_completed = get_object_or_404(NormalOrderCompleted, normal_order__pk=pk, normal_order__slug=normal_order_slug)
    normal_order_completed.approved = True
    normal_order_completed.save()
    return redirect(reverse("dashboard:admins:admin_orders_view"))