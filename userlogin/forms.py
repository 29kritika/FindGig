from django.contrib.auth.forms import UserCreationForm
from .models import User, Event, Post, Sponsor
from django import forms


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'type')
        widgets = {
            'type': forms.RadioSelect()
        }


class Bio(forms.ModelForm):
    class Meta:
        model = User
        fields = ('about_text', 'about_link')


class Name(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', )


class City(forms.ModelForm):
    class Meta:
        model = User
        fields = ('city', )


class Gender(forms.ModelForm):
    class Meta:
        model = User
        fields = ('gender', )
        widgets = {
            'type': forms.RadioSelect()
        }


class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'venue', 'date', 'startTime', 'endTime', 'video')


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('description', 'video')


class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = ('Amount', )