from django.urls import path

from . import views
from exambase import views as exambase_views

app_name = 'content'
urlpatterns = [
    path('', views.home, name='home'),
    path('gcse', views.gcse, name='gcse'),
    path('alevel', views.alevel, name='alevel'),
    path('about', views.about, name='about'),
    path('exambase', exambase_views.home, name='exambase'),
]
