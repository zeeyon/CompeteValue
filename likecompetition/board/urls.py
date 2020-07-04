from django.urls import path
from . import views

urlpatterns = [
    path('result/', views.result, name='result'),
]