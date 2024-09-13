from django.urls import path

from .views import LoginView, SignupView, LogoutView, UpdatePasswordView


app_name = "users"
urlpatterns = [
    path("login/", view=LoginView.as_view(), name="login"),
    path("logout/", view=LogoutView.as_view(), name="logout"),
    path("signup/", view=SignupView.as_view(), name="signup"),
    path("change-password/", view=UpdatePasswordView.as_view(), name="change_password"),
]
