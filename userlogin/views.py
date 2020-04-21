from django.shortcuts import render, redirect
from .models import User
from .forms import CustomUserCreationForm
from django.views.generic import CreateView


# _______________________Classes___________________________


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = '/home/'

    def __init__(self):
        self.template_name = 'signup.html'


# ____________________Functions____________________________


def index(request):
    return render(request, 'index.html')


def homePage(request):
    socialUserID = request.user.id
    try:
        user = User.objects.get(id=socialUserID)
        args = {'user': user, }
        if user.type == 'artist':
            return render(request, 'artist-home.html', args)
        if user.type == 'band':
            return render(request, 'band-home.html', args)
        return render(request, 'organiser-home.html', args)
    except:
        return redirect('Signup')
