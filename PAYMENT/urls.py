from django.urls import path
from . import views

urlpatterns = [
    path('mpesa/', views.index, name='index'),
]