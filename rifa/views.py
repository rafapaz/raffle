from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RaffleForm
from .models import Raffle
import datetime


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    raffles = Raffle.objects.all()

    return render(request, 'rifa/index.html', {'raffles': raffles})


def my_login(request):
    try:
        email = request.POST.get('email')
        psw = request.POST.get('psw')

        if email is None and psw is None:
            return render(request, 'login.html')

        username = User.objects.get(email=email.lower()).username
        user = authenticate(username=username, password=psw)

        if user is None:
            raise Exception('Shit!')

        login(request, user) 
        return redirect('index')
    except:
        context = {'message': 'Email or password not valid'}
        return render(request, 'login.html', context)


def my_logout(request):
    logout(request)
    return redirect('login')


def raffle_new(request):
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
    return render(request, 'rifa/raffle_edit.html', {'form': form, 'msg': form.errors})


def raffle_edit(request, pk):
    raffle = get_object_or_404(Raffle, pk=pk)
    if request.method == "POST":
        form = RaffleForm(request.POST, instance=raffle)

        if form.is_valid():
            raffle = form.save(commit=False)
            raffle.author = request.user
            raffle.published_date = datetime.datetime.now()
            raffle.save()
            return redirect('index')
    else:
        form = RaffleForm(instance=raffle)

    return render(request, 'rifa/raffle_edit.html', {'form': form})


def raffle_detail(request, pk):
    raffle = get_object_or_404(Raffle, pk=pk)
    context = {'raffle': raffle, 'range': range(1, raffle.qtd_num + 1)}
    return render(request, 'rifa/raffle_detail.html', context)
