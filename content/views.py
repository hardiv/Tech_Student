from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'content/home.html')


def gcse(request):
    return render(request, 'content/gcse.html')


def alevel(request):
    return render(request, 'content/alevel.html')


def supercurr(request):
    return render(request, 'content/supercurr.html')


def about(request):
    return render(request, 'content/about.html')
