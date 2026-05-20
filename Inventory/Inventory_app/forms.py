from django import forms
from .models import Product, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# PRODUCT FORM

class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = [
            'name',
            'price',
            'image',
            'description',
            'quantity'
        ]

        widgets = {

            'name': forms.TextInput(attrs={
                'class':'form-control'
            }),

            'price': forms.NumberInput(attrs={
                'class':'form-control'
            }),

            'image': forms.FileInput(attrs={
                'class':'form-control'
            }),

            'description': forms.Textarea(attrs={
                'class':'form-control'
            }),

            'quantity': forms.NumberInput(attrs={
                'class':'form-control'
            }),
        }


# REGISTER FORM

class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class':'form-control'
        })
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

        widgets = {

            'username': forms.TextInput(attrs={
                'class':'form-control'
            }),
        }


# PROFILE FORM

class ProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        fields = [
            'profile_image',
            'full_name',
            'phone',
            'address'
        ]

        widgets = {

            'full_name': forms.TextInput(attrs={
                'class':'form-control'
            }),

            'phone': forms.TextInput(attrs={
                'class':'form-control'
            }),

            'address': forms.Textarea(attrs={
                'class':'form-control'
            }),
        }