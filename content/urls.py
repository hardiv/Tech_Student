from django.urls import path

from . import views

app_name = 'content'
urlpatterns = [
    path('', views.home, name='home'),
    path('gcse', views.gcse, name='gcse'),
    path('alevel', views.alevel, name='alevel'),
    path('supercurr', views.supercurr, name='supercurr'),
    path('about', views.about, name='about'),
]
