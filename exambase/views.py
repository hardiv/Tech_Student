from django.shortcuts import render
from .models import *
from .forms import CreateQuestionForm


def dashboard(request):
    return render(request, 'exambase/dashboard.html')


def home(request):
    return render(request, 'exambase/home.html')


def account(request):
    return render(request, 'exambase/account.html')


def exams(request):
    return render(request, 'exambase/exams.html')


def tmua_topic_detail_view(request):
    topics = Topic.objects.all()
    qs = Question.objects.all()
    context = {
        'topic_objs': topics,
        'q_objs': qs
    }
    return render(request, 'exambase/tmua.html', context)


def question_create_view(request):
    form  = CreateQuestionForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    print(form.data)
    return render(request, 'exambase/create_question.html', context)
