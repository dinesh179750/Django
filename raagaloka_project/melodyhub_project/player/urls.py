from django.urls import path

from . import views

app_name = "player"

urlpatterns = [
    path("", views.index, name="index"),
    # audio / video are streamed with HTTP Range support so seeking works
    path("stream/<str:kind>/<str:filename>", views.stream, name="stream"),
]
