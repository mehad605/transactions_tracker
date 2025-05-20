# tracker/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction, UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount", "category", "comment", "date", "is_expense"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }


class BalanceForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["balance"]
