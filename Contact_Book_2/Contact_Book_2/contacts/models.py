from django.db import models
from django.urls import reverse

class Contact(models.Model):
    FAVOURITE = "favourite"
    PROFESSIONAL = "professional"
    PERSONAL = "personal"
    FLAG_CHOICES = [
        (FAVOURITE, "Favourite"),
        (PROFESSIONAL, "Professional"),
        (PERSONAL, "Personal"),
    ]

    first_name = models.CharField(max_length=80)
    middle_name = models.CharField(max_length=80, blank=True)
    last_name = models.CharField(max_length=80, blank=True)
    date_of_birth = models.DateField()
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=25)
    company = models.CharField(max_length=120, blank=True)
    company_email = models.EmailField(blank=True)
    flag = models.CharField(max_length=20, choices=FLAG_CHOICES, default=PERSONAL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["first_name", "last_name"]

    @property
    def full_name(self):
        return " ".join(part for part in [self.first_name, self.middle_name, self.last_name] if part).strip()

    def get_absolute_url(self):
        return reverse("contact_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.full_name
