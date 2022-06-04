import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.forms import ModelForm
from .models import Profile, Product
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(required=True, max_length=30, min_length=3,
                               help_text="Latin lowercase letters, underscores and digits only. At least 3 "
                                         "characters.")
    image = forms.ImageField(required=False)
    email = forms.EmailField(required=True, validators=[EmailValidator(message="Email is invalid")])

    address = forms.CharField(required=False)
    first_name = forms.CharField(required=False, help_text="First letter should be uppercase. Only latin characters. ")
    last_name = forms.CharField(required=False, help_text="First letter should be uppercase. Only latin characters. ")
    captcha = CaptchaField()

    def clean_username(self):
        data = self.cleaned_data['username']
        if not re.match("^[a-zA-Z0-9]{3,30}$", data):
            raise ValidationError("Username is invalid")
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if data and not re.match("^[A-Z][a-z]+$", data):
            raise ValidationError("First name is invalid")
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if data and not re.match("^[A-Z][a-z]+$", data):
            raise ValidationError("Last name is invalid")
        return data

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic', "address", "work_place", "email")


class WriteNewsForm(forms.Form):
    topic = forms.CharField(label='Topic of message', max_length=200)
    text = forms.CharField(label='Your news/discount', widget=forms.Textarea)
    captcha = CaptchaField()


class ProductNewForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'image', 'description', 'price', 'available', 'stock']
    captcha = CaptchaField()



