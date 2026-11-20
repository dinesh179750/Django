from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "first_name", "middle_name", "last_name", "date_of_birth",
            "email", "phone", "company", "company_email", "flag",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "flag": forms.Select(),
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = "".join(ch for ch in phone if ch.isdigit())
        if len(digits) < 7 or len(digits) > 15:
            raise forms.ValidationError("Enter a phone number containing 7 to 15 digits.")
        return phone
