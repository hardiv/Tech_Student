from django.shortcuts import render
from .forms import *
from exambase.utils import *


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
    questions = Question.objects.all()
    context = {
        'topic_objs': topics,
        'question_objs': questions
    }
    return render(request, 'exambase/tmua.html', context)


def question_create_view(request):
    form = CreateQuestionForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    print(form.data)
    return render(request, 'exambase/create_question.html', context)


def question_detail_view(request, q_id=1):
    form = QuestionAnswerForm()
    context = {
        'question_id': q_id,
        'image_path': get_q_image_path(q_id),
        'question': Question.objects.get(pk=q_id),
        'form': form,
    }
    return render(request, 'exambase/question.html', context)
