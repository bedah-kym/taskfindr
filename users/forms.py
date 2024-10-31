from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import profile,Cashaccount
from django.core.validators import RegexValidator

class registration_form (UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    
    phone = forms.IntegerField(
        validators=[RegexValidator(
            r"^(?:254|\+254|0)?([17]\d{1})(\d{7})$",
            'Enter a valid Safaricom number'
        )],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        })
    )
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            
            'type':'password'
        })
    )
    
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'RE-Enter your password',
            
            'type':'password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
            }),
        }

class updateuser(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class updateprofile(forms.ModelForm):
    phone_number = forms.IntegerField(
        validators=[RegexValidator(
            r"^(?:254|\+254|0)?([17]\d{1})(\d{7})$", 
            'Enter a valid Safaricom number'
        )],
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = profile
        fields = ['image', 'phone_number']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class activationform(forms.ModelForm):
    mpesa_code= forms.CharField(max_length=10, validators=[RegexValidator(r"^[0-9|A-Z]{10}$",'invalid code')])
    class Meta:
        model= Cashaccount
        fields=['mpesa_code']
