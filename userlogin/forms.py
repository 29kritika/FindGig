from django.contrib.auth.forms import UserCreationForm
from .models import User
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