from django.shortcuts import render, redirect
from .models import User
from .forms import CustomUserCreationForm, Bio, Name, City, Gender
from django.http import Http404
from django.views.generic import CreateView


# _______________________Classes__________________________


# ____________________Functions____________________________


def index(request):
    return render(request, 'index.html')


def checkArtist(user):
    if user.type == 'artist':
        return
    raise Http404('not allowed ')


def homePage(request):
    socialUser = request.user
    try:
        user = User.objects.get(user=socialUser)
        args = {'user': user, }
        if user.type == 'artist':
            return render(request, 'artist-home.html', args)
        if user.type == 'band':
            return render(request, 'band-home.html', args)
        return render(request, 'organiser-home.html', args)
    except:
        return redirect('Signup')


def signUp(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            User.objects.update_or_create(
                user=request.user,
                type=user.type,
                username=user.username,
                name=user.name
            )
            return redirect('/')
        else:
            print("why dude")
    else:
        form = CustomUserCreationForm
    arg = {'form': form}
    return render(request, 'signup.html', arg)

def asettings(request):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    checkArtist(user)
    return render(request, 'artists/asettings.html')


def change_bio(request):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    if request.method == 'POST':
        form = Bio(request.POST)
        if form.is_valid():
            bio = form.save(commit=False)
            user.about_text = bio.about_text
            user.about_link = bio.about_link
            user.save()
            return redirect('Home')
        else:
            print("why dude")
    else:
        form = Bio()
    arg = {'form': form,}
    return render(request, 'change_bio.html', arg)


def change_name(request):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    if request.method == 'POST':
        form = Name(request.POST)
        if form.is_valid():
            name = form.save(commit=False)
            user.name = name.name
            user.save()
            return redirect('Home')
        else:
            print("why dude")
    else:
        form = Name()
    arg = {'form': form, }
    return render(request, 'change_name.html', arg)


def change_city(request):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    if request.method == 'POST':
        form = City(request.POST)
        if form.is_valid():
            city = form.save(commit=False)
            user.city = city.city
            user.save()
            return redirect('Home')
        else:
            print("why dude")
    else:
        form = City()
    arg = {'form': form, }
    return render(request, 'change_city.html', arg)

def change_gender(request):
    socialUser = request.user
    user = User.objects.get(user=socialUser)
    if request.method == 'POST':
        form = Gender(request.POST)
        if form.is_valid():
            name = form.save(commit=False)
            user.gender = name.gender
            user.save()
            return redirect('Home')
        else:
            print("why dude")
    else:
        form = Gender()
    arg = {'form': form, }
    return render(request, 'change_city.html', arg)