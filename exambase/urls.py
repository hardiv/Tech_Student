from django.urls import path

from . import views

app_name = 'exambase'
urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login, name="login")
]
