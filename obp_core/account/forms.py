from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from captcha.fields import CaptchaField

from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
    UserCreationForm as BaseUserCreationForm,
    PasswordResetForm as BasePasswordResetForm,
)


class AuthenticationForm(BaseAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RegisterForm(BaseUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RegistrationForm(BaseUserCreationForm):
    username = forms.RegexField(
        label="Username",
        max_length=30,
        regex=r"^[\w.@+-]+$",
        error_messages={
            "invalid": "This value may contain only letters, numbers and @/./+/-/_ characters."
        },
    )

    email = forms.EmailField(label="Email")

    captcha = CaptchaField(
        label="Security Code",
        help_text="Please enter the characters shown beside.",
    )

    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        label=mark_safe(
            'I have read and agree to the <a target="_blank" href="/about/terms-and-conditions/">terms and conditions</a> and <a target="_blank" href="/about/data-use-policy/">data use policy</a>'
        ),
        error_messages={
            "required": "You must agree to the terms and conditions and data use policy to register."
        },
    )
    # TODO: implement own loqic without password repeat
    password2 = forms.CharField(widget=forms.HiddenInput, required=False)

    field_order = ["email", "username", "password1", "password2", "captcha", "tos"]

    class Meta:
        model = get_user_model()
        fields = ("email", "username")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # TODO: implement own loqic without password repeat
    def clean_password2(self):
        return True

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("This e-mail address is already in use.")

        return email


class PasswordRequestResetForm(BasePasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]

        qs = get_user_model().objects.filter(email=email)

        if not qs.exists():
            raise ValidationError("No account with given e-mail address.")

        if qs.count() > 1:
            raise ValidationError(
                "We have multiple accounts registered with this e-mail address. Please contact our support"
            )

        if not qs.first().has_usable_password():
            raise ValidationError(
                "This e-mail address is registered via a 3-rd party login. You cannot reset the password."
            )

        return email


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(label="New password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="New password (confirm)", widget=forms.PasswordInput
    )

    error_messages = {"password_mismatch": "The two passwords didn't match."}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if not password1 == password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"], code="password_mismatch"
            )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["password1"])
        if commit:
            get_user_model().objects.filter(pk=self.user.pk).update(
                password=self.user.password
            )
        return self.user
