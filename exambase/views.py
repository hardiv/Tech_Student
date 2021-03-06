from django.shortcuts import render
from .forms import *
from exambase.utils import *
from itertools import chain


def dashboard_view(request):
    user  = request.user
    attempts = get_attempts(user)
    strong_topics, weak_topics, recommended_questions = [], [], []
    if attempts is not None:
        strong_topics, weak_topics = get_strong_and_weak_topics(attempts)
        recommended_questions = recommend_questions(weak_topics, attempts)
    context = {
        'user': user,
        'strong_topics': strong_topics,
        'weak_topics': weak_topics,
        'recommended_questions': recommended_questions
    }
    return render(request, 'exambase/dashboard.html', context)


def home(request):
    return render(request, 'exambase/home.html')


def account(request):
    return render(request, 'exambase/account.html')


def exam_browser_view(request):
    context = {
        'exams': get_paper_names()
    }
    return render(request, 'exambase/exam_browser.html', context)


def exam_question_browser_view(request, exam_name):
    topics = Topic.objects.all()
    exam_name = exam_name.upper()
    papers = Exam.objects.filter(paper_name=exam_name)
    questions = []
    for paper in papers:
        questions = list(chain(questions, Question.objects.filter(exam=paper)))
    context = {
        'topic_objs': topics,
        'question_objs': questions,
        'exam_name': exam_name
    }
    return render(request, 'exambase/exam_question_browser.html', context)


def create_question_view(request):
    form = CreateQuestionForm(request.POST or None)
    success = None
    img_path = "format EXAM_20XX_POSITION.jpg"
    if form.is_valid():
        topic, exam, pos = form.cleaned_data['topic'], form.cleaned_data['exam'], form.cleaned_data['exam_position']
        if does_question_exist(topic, exam, pos):
            success = False
        else:
            question = form.save()
            generate_options(form, question)
            success = True
            img_path = f"name {get_q_img_rel_path(question.id)}"

    context = {
        'form': form,
        'success': success,
        'path': img_path
    }
    return render(request, 'exambase/create_question.html', context)


def question_detail_view(request, q_id):
    form = QuestionAnswerForm(request.POST or None, q_id=q_id)
    attempt, option, correctAns = save_attempt(q_id, form, request.user)

    context = {
        'question_id': q_id,
        'image_path': get_q_image_path(q_id),
        'question': Question.objects.get(pk=q_id),
        'correct': correctAns,
        'form': form,
        'selection': option,
        'attempt': attempt,
    }

    return render(request, 'exambase/question.html', context)
