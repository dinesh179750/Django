from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('std',views.student,name='std'),
    path('sap',views.book_store,name='sap')
]