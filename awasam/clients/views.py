from typing import Any
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from awasam.orders.forms import CourseAddForm, NormalOrderForm
from awasam.orders.models import Course, Normal, NormalOrderFile
from django.contrib.auth.mixins import LoginRequiredMixin
from awasam.payments.models import Transaction
from django.db.models import Sum, Q
from django.contrib import messages
# Create your views here.

class ProfileLoginRequiredView(LoginRequiredMixin):
    def get_profile(self):
        return self.request.user.profile_user


# Create your views here.

class DashboardMixinView(ProfileLoginRequiredView, TemplateView):
    template_name = ""
    
    def get_transactions(self):
        return Transaction.objects.prefetch_related("client").filter(client=self.get_profile())

    def get_order_items(self):
        return Normal.objects.prefetch_related("client").filter(client=self.get_profile()).filter(is_active=True)
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_profile()
        context["orders"] = self.get_order_items()
        context["transaction_balance"] = self.get_transactions().aggregate(amount=Sum("amount"))["amount"]
        context["courses"] = Course.objects.prefetch_related("client").filter(
            client=self.get_profile()).filter(is_active=True)
        return context


class HomeView(DashboardMixinView):
    template_name = "dashboard/client/pages/home.html"


client_home_view = HomeView.as_view()

class PlaceOrderView(ProfileLoginRequiredView, TemplateView):
    template_name = "dashboard/client/pages/add_order.html"
    form_class = NormalOrderForm
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.client = self.get_profile()
            instance.save()
            form.save()
            instance.save()
            # Save multiple files
            files = self.request.FILES.getlist('uploads')
            for file in files:
                NormalOrderFile.objects.create(normal_order=instance, upload=file)
            return redirect("dashboard:payments:orders:normal_order_payment_view")
        print(form.errors.as_data)
        return render(self.request, self.template_name, {"form": form, "success": False})

client_add_order_view = PlaceOrderView.as_view()


class PlaceExamOrderView(ProfileLoginRequiredView, TemplateView):
    template_name = "dashboard/client/pages/add_exam.html"

client_add_exam_order_view = PlaceExamOrderView.as_view()

class PlaceCourseOrderView(ProfileLoginRequiredView, TemplateView):
    template_name = "dashboard/client/pages/add_course.html"
    form_class  = CourseAddForm
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.client = self.get_profile()
            instance.save()
            form.save()
            instance.save()
            return redirect("dashboard:clients:courses_list_view")
        return redirect(request.GET.get("HTTP_REFERER", reverse("dashboard:clients:home")))

client_add_course_order_view = PlaceCourseOrderView.as_view()


class CoursesListView(DashboardMixinView):
    template_name = "dashboard/client/pages/courses.html"
    

class RecommendationView(ProfileLoginRequiredView, TemplateView):
    template_name = "dashboard/client/pages/recommendations.html"

recommendation_view = RecommendationView.as_view()


from awasam.dashboard.views import DashboardAccountView
from awasam.users.forms import PasswordUpdateForm


class ClientDashboardAccountView(DashboardAccountView, DashboardMixinView):
    template_name = "dashboard/client/account/index.html"
    change_password_form = PasswordUpdateForm
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context["change_password_form"] = self.change_password_form()
        return context
    

client_dashboard_account = ClientDashboardAccountView.as_view()