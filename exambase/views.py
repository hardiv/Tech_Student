from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'exambase/dashboard.html')


def home(request):
    return render(request, 'exambase/home.html')


def account(request):
    return render(request, 'exambase/account.html')


def exams(request):
    return render(request, 'exambase/exams.html')


def tmua(request):
    return render(request, 'exambase/tmua.html')
