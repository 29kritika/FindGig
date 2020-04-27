from django.shortcuts import render, redirect
from .models import User
from .forms import CustomUserCreationForm
from django.views.generic import CreateView


# _______________________Classes__________________________


# ____________________Functions____________________________


def index(request):
    return render(request, 'index.html')


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
