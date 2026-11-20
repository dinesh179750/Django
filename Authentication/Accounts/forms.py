# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField

class RegistrationForm(UserCreationForm):
    pass

class RecaptchaForm(forms.Form):
    # Change 'Captcha' to lowercase 'captcha'
    captcha = ReCaptchaField() 
