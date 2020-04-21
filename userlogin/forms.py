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
