from django import forms
from .models import To_Do

class To_do_Forms(forms.ModelForm):
    class Meta:
        model = To_Do
        exclude = ('user',)