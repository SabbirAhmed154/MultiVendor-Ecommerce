from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomerRegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20)
    address = forms.CharField(
        widget=forms.Textarea,
        required=False
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'phone',
            'address',
            'password1',
            'password2',
        ]


class SellerRegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20)
    address = forms.CharField(
        widget=forms.Textarea,
        required=False
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'phone',
            'address',
            'password1',
            'password2',
        ]