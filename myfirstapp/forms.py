from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm, ModelChoiceField, CheckboxSelectMultiple
from django.db import transaction
import datetime

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = [ 'size', 'sauce', 'crust', 'cheese', 'topping']
        widgets = {
            'size': forms.Select(attrs={'class':"rounded bg-dark text-white border-light "}),
            'sauce': forms.Select(attrs={'class':"rounded bg-dark text-white border-light"}),
            'crust': forms.Select(attrs={'class':"rounded bg-dark text-white border-light"}),
            'cheese': forms.Select(attrs={'class':"rounded bg-dark text-white border-light"}),
            'topping': forms.CheckboxSelectMultiple(attrs={'class':"rounded bg-dark text-white border-light"}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'street_address', 'city', 'county', 'eircode', 'phone', 'card_number', 'card_expiry', 'card_cvc', 'delivery_date', 'delivery_time']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'pattern': '[A-Za-z ]+', 'class':"rounded bg-dark text-white border-light"}),
            'street_address': forms.TextInput(attrs={'placeholder': '123 Habibi Lane', 'class':"rounded bg-dark text-white border-light"}),
            'city': forms.TextInput(attrs={'placeholder': 'Habibi City', 'pattern': '[A-Za-z ]+', 'class':"rounded bg-dark text-white border-light"}),
            'county': forms.TextInput(attrs={'placeholder': 'Meath', 'pattern': '[A-Za-z ]+', 'class':"rounded bg-dark text-white border-light"}),
            'eircode': forms.TextInput(attrs={'placeholder': 'A69C72J', 'pattern': '[A-Z0-9]{7}', 'class':"rounded bg-dark text-white border-light"}),
            'phone': forms.TextInput(attrs={'placeholder': '0831234123', 'pattern': '[0-9]{10}', 'class':"rounded bg-dark text-white border-light"}),
            'card_number': forms.TextInput(attrs={'placeholder': '1234 1234 1234 1234', 'pattern': '[0-9]{4} [0-9]{4} [0-9]{4} [0-9]{4}', 'class':"rounded bg-dark text-white border-light"}),
            'card_expiry': forms.TextInput(attrs={'placeholder': 'MM/YY', 'pattern': '[0-9]{2}/[0-9]{2}', 'class':"rounded bg-dark text-white border-light"}),
            'card_cvc': forms.TextInput(attrs={'placeholder': '123', 'pattern': '[0-9]{3}', 'class':"rounded bg-dark text-white border-light"}),
            'delivery_date': forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today().strftime('%Y-%m-%d'), 'class':"rounded bg-dark text-white border-light"}),
            'delivery_time': forms.TimeInput(attrs={'type': 'time', 'class':"rounded bg-dark text-white border-light"}),

        }

    def clean(self):
        cleaned_data = super().clean()
        card_number = cleaned_data.get('card_number')
        card_expiry = cleaned_data.get('card_expiry')
        card_cvc = cleaned_data.get('card_cvc')
        if len(card_number) != 19:
            raise forms.ValidationError("Card number must be 16 digits long")
        if len(card_expiry) != 5:
            raise forms.ValidationError("Card expiry must be in the format MM/YY")
        if len(card_cvc) != 3:
            raise forms.ValidationError("Card CVC must be 3 digits long")





class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.email = self.cleaned_data['username']
        user.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
