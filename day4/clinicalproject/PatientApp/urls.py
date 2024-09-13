from django.urls import path
from . import views

urlpatterns = [
    path('', views.Patient_list, name='Patient_list'),
    path('create/', views.Patient_create, name='Patient_create'),
    path('update/<int:id>/', views.Patient_update, name='Patient_update'),
    path('delete/<int:id>/', views.Patient_delete, name='Patient_delete'),
]