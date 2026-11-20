from django.urls import path
from . import views
urlpatterns=[
    path('1',views.home,name='home'),
    path('2',views.santoor,name='santoor'),
    path('3',views.star,name='star'),
    path('4',views.nirma,name='nirma'),
    path('5',views.glucose,name='glucose'),
    path('6',views.gems,name='gems'),
    path('7',views.centerfruit,name='centerfruit')
]