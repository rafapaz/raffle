from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import RaffleForm
from .models import Raffle, Choice, Reputation, Question, Image
import datetime


# Aux functions

def reputation(user):
    reps = Reputation.objects.filter(user_to=user)
    scores = [r.score for r in reps]
    score = sum(scores) / float(len(scores))
    return score


# Views

def index(request):

    raffles = Raffle.objects.all()
    # perc = {r.id: r.choices.count()/r.qtd_num for r in raffles}
    return render(request, 'rifa/index.html', {'raffles': raffles})


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
            return redirect('raffle_image', raffle.id)
    else:
        form = RaffleForm()

    return render(request, 'rifa/raffle_edit.html', {'form': form, 'msg': form.errors})


def raffle_edit(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

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
    choices_num = [c.number for c in raffle.choices.all()]
    score = reputation(raffle.author)

    context = {'raffle': raffle, 'range': range(1, raffle.qtd_num + 1), 'choices_num': choices_num, 'score': score}
    return render(request, 'rifa/raffle_detail.html', context)


def raffle_image(request, raffle_id):
    if not request.user.is_authenticated:
        return redirect('login')

    raffle = get_object_or_404(Raffle, pk=raffle_id)
    if raffle.author != request.user:
        return redirect('index')

    context = {'raffle': raffle}

    if request.method == "POST":
        files = request.FILES.getlist('img')
        for f in files:
            image = Image()
            image.raffle = raffle
            image.img = f
            image.save()

    return render(request, 'rifa/raffle_image.html', context)


def raffle_edit_image(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        image_id = request.POST.get('main')
        ids_remov = request.POST.getlist('delete')
        image = get_object_or_404(Image, pk=image_id)

        if image.raffle.author != request.user:
            return redirect('index')

        all_images = image.raffle.images.all()
        for img in all_images:
            img.main = False
            img.save()

        image.main = True
        image.save()

        for id in ids_remov:
            Image.objects.filter(id=id).delete()

        return redirect('raffle_image', image.raffle.id)

    return redirect('index')


def choose(request, raffle_id, num):
    raffle = get_object_or_404(Raffle, pk=raffle_id)
    choice = Choice()
    choice.user = request.user
    choice.number = num
    choice.date = datetime.datetime.now()
    choice.raffle = raffle
    choice.save()
    return redirect('index')


def rate(request, raffle_id, user_id):
    raffle = get_object_or_404(Raffle, pk=raffle_id)
    otherUser = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        score = request.POST.get('rating')
        comment = request.POST.get('comment')
        rep = Reputation()
        rep.user_from = request.user
        rep.user_to = otherUser
        rep.score = score
        rep.raffle = raffle
        rep.comment = comment
        rep.save()
        return redirect('index')
    
    context = {'raffle': raffle, 'otherUser': otherUser}
    return render(request, 'rifa/rate.html', context)


def ask(request, raffle_id):
    if not request.user.is_authenticated:
        return redirect('login')

    raffle = get_object_or_404(Raffle, pk=raffle_id)

    if request.method == "POST":
        question = Question()
        question.question = request.POST.get('question')
        question.raffle = raffle
        question.user = request.user
        question.save()
        return redirect('raffle_detail', raffle.id)
    
    return redirect('index')


def answer(request, question_id):
    if not request.user.is_authenticated:
        return redirect('login')

    question = get_object_or_404(Question, pk=question_id)
    if question.raffle.author != request.user:
        return redirect('index')

    if request.method == "POST":
        question.answer = request.POST.get('answer')
        question.save()
        return redirect('raffle_detail', question.raffle.id)
    
    return redirect('index')
