from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api_02/', views.api_02, name='api_02'),
]