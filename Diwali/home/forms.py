from django import forms
from .models import Crackers 
from .models import Sweets
from .models import Gifts

class CrackersForm(forms.ModelForm):  
    class Meta:
        model = Crackers  
        fields = '__all__'

class sweetsform(forms.ModelForm):
    class Meta:
        model = Sweets
        fields = '__all__'

class Giftsform(forms.ModelForm):
    class Meta:
        model = Gifts
        fields = '__all__'