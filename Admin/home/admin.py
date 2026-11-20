from django.contrib import admin
from .models import teams
# Register your models here.
# admin.site.register(teams)


@admin.register(teams)
class IPLTeamAdmin(admin.ModelAdmin):
    list_display=["name","fullform","owner","cap","coach","homeground_loc","cups","sponsors","reached_final","networth_of_team"]
    list_display_links=["name","fullform","owner","cap","coach","homeground_loc","cups","sponsors","reached_final","networth_of_team"]