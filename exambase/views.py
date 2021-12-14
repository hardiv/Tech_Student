from django.shortcuts import render
from .models import Topic


def dashboard(request):
    return render(request, 'exambase/dashboard.html')


def home(request):
    return render(request, 'exambase/home.html')


def account(request):
    return render(request, 'exambase/account.html')


def exams(request):
    return render(request, 'exambase/exams.html')


def tmua_topic_detail_view(request):
    objs = Topic.objects.all()
    context = {
        'topic_objs': objs
    }
    return render(request, 'exambase/tmua.html', context)
