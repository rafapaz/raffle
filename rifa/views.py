from django.shortcuts import render

def index(request):
    return render(request, 'rifa/index.html')
