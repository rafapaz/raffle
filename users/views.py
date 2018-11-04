from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Aux functions

def my_authenticate(request, username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        raise Exception('Cannot authenticate!')
    login(request, user)


# Views

def signup(request):
    try:
        if request.method == "POST":

            User.objects.create_user(username=request.POST.get('email'),
                                            email=request.POST.get('email'),
                                            password=request.POST.get('psw'),
                                            first_name=request.POST.get('first_name'),
                                            last_name=request.POST.get('last_name'))

            # my_authenticate(request, user.username, user.password)
            return redirect('login')

    except Exception as e:
        context = {'message': str(e)}
        return render(request, 'users/signup.html', context)

    return render(request, 'users/signup.html')


def my_login(request):
    try:
        email = request.POST.get('email')
        psw = request.POST.get('psw')

        if email is None and psw is None:
            return render(request, 'users/login.html')

        username = User.objects.get(email=email.lower()).username
        my_authenticate(request, username, psw)
        return redirect('index')

    except Exception:
        context = {'message': 'Email or password not valid'}
        return render(request, 'users/login.html', context)


def my_logout(request):
    logout(request)
    return redirect('index')


def profile(request, pk):
    someUser = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'someUser': someUser})