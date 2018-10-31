from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RaffleForm
import datetime


def index(request):
    if not request.user.is_authenticated:
        return redirect('login') 

    return render(request, 'rifa/index.html')


def my_login(request):
    try:
        email = request.POST.get('email')
        psw = request.POST.get('psw')

        if email is None and psw is None:
            return render(request, 'rifa/login.html')

        username = User.objects.get(email=email.lower()).username
        user = authenticate(username=username, password=psw)

        if user is None:
            raise Exception('Shit!')

        login(request, user) 
        return redirect('index')
    except:
        context = {'message': 'Email or password not valid'}
        return render(request, 'rifa/login.html', context)


def my_logout(request):
    logout(request)
    return redirect('login')


def create_raffle(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    
    if request.method == "POST":
        form = RaffleForm(request.POST)

        if form.is_valid():
            raffle = form.save(commit=False)
            raffle.author = request.user
            raffle.pub_date = datetime.datetime.now()
            raffle.save()
            return redirect('index')

    form = RaffleForm()
    return render(request, 'rifa/edit_raffle.html', {'form': form, 'msg': form.errors})
