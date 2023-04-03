from django.contrib import admin
from django.urls import include, path
from .views import Dashboard

urlpatterns = [

    path('dashboard/', Dashboard.as_view(), name = 'dashboard'),



]