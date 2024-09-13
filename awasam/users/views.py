import json
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView
from django.utils.translation import gettext_lazy as _
from .forms import UserCreationForm, UserLoginForm
from .utils import JavascriptPostCleanFormViewMixin
from awasam.users.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import messages

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PasswordUpdateForm  # Assuming you have a form for updating the password

class LoginView(TemplateView):
    template_name = "account/auth/login.html"
    form_class = UserLoginForm


    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = UserLoginForm(request.POST)
        context["form"] = form
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get("email"), password=form.cleaned_data.get("password"))
            if user is not None:
                login(request, user)
                if (request.user.account_type == "Student"):
                    return redirect(reverse("dashboard:clients:home"))
                elif (request.user.account_type == "Writer"):
                    return redirect(reverse("dashboard:writers:home"))
                elif (request.user.account_type == "Editor"):
                    return redirect(reverse("dashboard:editors:home"))
                elif (request.user.account_type == "Admin"):
                    return redirect(reverse("dashboard:admins:home"))
                else:
                    return redirect(reverse("home"))
            messages.error(request,"No use with the provided credentials")
            return render(request, self.template_name, context)
        return render(request, self.template_name, context)

class SignupView(JavascriptPostCleanFormViewMixin, FormView):
    template_name = "account/auth/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("users:login")
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        data = self.ajax_filter_formatted_data(request)
        form = self.form_class(data=data)
        if form.is_valid():
            return self.form_valid(form)
        return JsonResponse({"errors": "User with this Email Address already exists"})

    def form_valid(self, form:UserCreationForm):
        user = User.objects.filter(email=form.cleaned_data.get("email"))
        if user.exists():
            return JsonResponse({"errors": "User with email already exists"})
        user = User.objects.create_user(
            email=form.cleaned_data.get("email"),
            password=form.cleaned_data.get("password"),
        )
        user.account_type = form.cleaned_data.get("account_type")
        user.save()
        return JsonResponse({"message": "User created successfully", "url": reverse("users:login")})
    

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("users:login")
    

class UpdatePasswordView(LoginRequiredMixin, View):
    form_class = PasswordUpdateForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        previous_url = request.META.get('HTTP_REFERER')  # Get the previous URL

        if form.is_valid():
            user = request.user
            # Check if the old password is correct
            if user.check_password(form.cleaned_data.get("old_password")):
                # Check if new password and confirm password match
                if form.cleaned_data.get("new_password") == form.cleaned_data.get("confirm_new_password"):
                    # Update password and save user
                    user.set_password(form.cleaned_data.get("new_password"))
                    user.save()

                    # Keep the user logged in after password change
                    update_session_auth_hash(request, user)
                    messages.success(request, 'Your password has been updated.')
                    return redirect(previous_url)
                else:
                    # New password and confirm password do not match
                    messages.info(request, "Your new password and confirm password did not match.")
            else:
                # Old password is incorrect
                messages.warning(request, "Invalid old password.")
        
        # If the form is not valid or there's an error, redirect to the previous page
        return redirect(previous_url)
