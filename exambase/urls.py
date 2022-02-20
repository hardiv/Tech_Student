from django.urls import path
from . import views

app_name = 'exambase'
urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard', views.dashboard, name='dashboard'),
    path('account', views.account, name="account"),
    path('exam_browser', views.exam_browser_view, name="exam_browser"),
    path('<str:exam_name>/', views.exam_question_browser_view, name="exam_q_browser"),
    path('create', views.create_question_view, name="create"),
    path('question/<str:q_id>', views.question_detail_view, name="question")
]
