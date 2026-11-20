
from django.urls import path
from . import views

urlpatterns = [
    # LIST ALL CASES
    path('', views.list_data, name='list_data'),

    # ADD CASE
    path('case/', views.add_case, name='case'),

    # ADD AGENT
    path('agent/', views.add_agent, name='agent'),

    # SINGLE CASE DETAILS
    path('single/<int:pk>/', views.single_data, name='single'),

    # EDIT CASE
    path('edit/<int:id>/', views.edit, name='update'),

    # DELETE CASE
    path('delete/<int:vk>/', views.delete_case, name='del'),
]