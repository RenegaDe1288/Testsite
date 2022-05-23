from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    """Форма регистрации"""

    class Meta:
        model = User
        fields = ['username', 'last_name', 'first_name', 'password1', 'password2']


class AddSkillForm(forms.Form):
    """Форма добавления навыка"""
    tag = forms.CharField(max_length=50, min_length=3, required=False, label='Добавить тег')
    skill = forms.CharField(max_length=50, min_length=3, required=False, label='Добавить навык')
