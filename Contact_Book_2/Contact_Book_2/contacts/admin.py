from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "email", "flag", "date_of_birth")
    list_filter = ("flag",)
    search_fields = ("first_name", "middle_name", "last_name", "phone", "email", "company")
