# Generated for Contact Book 2.0
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=80)),
                ("middle_name", models.CharField(blank=True, max_length=80)),
                ("last_name", models.CharField(blank=True, max_length=80)),
                ("date_of_birth", models.DateField()),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("phone", models.CharField(max_length=25)),
                ("company", models.CharField(blank=True, max_length=120)),
                ("company_email", models.EmailField(blank=True, max_length=254)),
                ("flag", models.CharField(choices=[("favourite", "Favourite"), ("professional", "Professional"), ("personal", "Personal")], default="personal", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["first_name", "last_name"]},
        ),
    ]
