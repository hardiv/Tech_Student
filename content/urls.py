from django.urls import path

from . import views

app_name = 'content'
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home)
]
