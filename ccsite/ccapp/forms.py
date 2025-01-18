from django import forms
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    """Form for creating a new user."""

    firstname = forms.CharField(max_length=30, required=False)
    lastname = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, required=True)
    category = forms.RadioSelect(
        choices=[("student", "Student"), ("instructor", "Instructor")]
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "category",
            "firstname",
            "lastname",
            "password1",
            "password2",
        )
