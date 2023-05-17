from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import profile,Cashaccount
from django.core.validators import RegexValidator

class registration_form (UserCreationForm):
        email=forms.EmailField(),
        phone = forms.IntegerField(validators=[RegexValidator(r"^(?:254|\+254|0)?([17]\d{1})(\d{7})$",'enter a valid safaricom number')]) #add validators
        class Meta:
            model=User
            fields=[
            'username',
            'email',
            'phone',
            'password1',
            'password2'
            ]


class updateuser(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email']

class updateprofile(forms.ModelForm):
    phone_number = forms.IntegerField(
         validators=[RegexValidator(
         r"^(?:254|\+254|0)?([17]\d{1})(\d{7})$",
         'enter a valid safaricom number')
         ]
        )
    class Meta:
        model=profile
        fields=['image','phone_number']

class activationform(forms.ModelForm):
    mpesa_code= forms.CharField(max_length=10, validators=[RegexValidator(r"^[0-9|A-Z]{10}$",'invalid code')])
    class Meta:
        model= Cashaccount
        fields=['mpesa_code']
