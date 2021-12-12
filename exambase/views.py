from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'exambase/dashboard.html')


def home(request):
    return render(request, 'exambase/home.html')
