from django.contrib.auth import forms as admin_forms
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Profile, User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """


    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = ("email", "account_type")
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }

class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control rounded-end","placeholder": "Password"}))

class UserCreationForm(forms.ModelForm):
    account_type = forms.ChoiceField(
        widget=forms.Select(
            attrs={
            "class": "form-control rounded-end",
            "data-placeholder":"Select Parent",
            "tabindex":"-1",
            },
        ),
        choices=(
            ("Student","Student"),
            ("Writer","Writer"),
            ("Editor","Editor"),
        ),
        initial="Student",
    )
    
    class Meta:
        model = User
        fields = (
            "email",
            "account_type",
            "password",
        )
        widgets = {
            "email":  forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"}),
            "password": forms.PasswordInput(attrs={"class": "form-control rounded-end","placeholder": "Password"}),
        }
        
        
class ProfileUpdateForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    phone_number = forms.CharField(required=False, widget=forms.NumberInput(attrs={"class": "form-control","placeholder": "+1 908 **** ****"}))
    bank_account_number = forms.CharField(required=False, widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Bank Account Number"}))
    
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "placeholder":"About myself", "rows":5}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control",}))
    
    class Meta:
        model = Profile
        fields = [
            "full_name",
            "phone_number",
            "bank_account_number",
            "bio",
            "avatar",
        ]
        
class PasswordUpdateForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input100 form-control", "placeholder": ""}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input100 form-control", "placeholder": ""}))
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input100 form-control", "placeholder": ""}))
    