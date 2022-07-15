from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('andre/', views.grafico_teste, name='grafico_teste'),
]
