from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.views import LogoutView, LoginView
from .forms import RegistrationForm, AddSkillForm
from .models import *


class CandidatesList(ListView):
    """Отображение списка кандидатов"""
    model = Candidate
    template_name = 'main.html'
    context_object_name = 'candidates'


def show_account(request):
    """Отображение данных кандидата"""
    if request.method == 'POST':
        data = request.POST
        user = Candidate.objects.get(name=request.user.username)
        if 'delete' in data:
            skill = Skill.objects.get(name__startswith=data['delete'])
            tag = skill.tag.id
            count = Skill.objects.filter(candidate__id=user.id, tag=tag).count()
            if count == 1:
                tag = Tag.objects.get(name=skill.tag)
                user.tag.remove(tag.id)
            user.skill.remove(skill.id)
            return redirect('/account')
        elif 'choice' in data:
            data = list(data['choice'].split(','))
            tag = Tag.objects.get(name__startswith=data[1])
            skill = Skill.objects.get(name__startswith=data[0])
            user.tag.add(tag)
            user.skill.add(skill)
            return redirect('/account')
        elif 'add' in data:
            new_form = AddSkillForm(request.POST)
            new_form.get_context()
            tag = new_form.cleaned_data.get('tag')
            skill = new_form.cleaned_data.get('skill')
            if Skill.objects.filter(name=skill):
                message = 'Данный  навык уже существует'
                return HttpResponse(message)
            elif tag == '' or skill == '':
                message = 'Не введено обязательное поле'
                return HttpResponse(message)
            elif not Tag.objects.filter(name=tag):
                new_tag = Tag.objects.create(name=tag)
            elif Tag.objects.filter(name=tag):
                new_tag = Tag.objects.get(name=tag)
            new_skill = Skill.objects.create(name=skill, tag=new_tag)
            user.tag.add(new_tag)
            user.skill.add(new_skill)
        return redirect('/account')
    else:
        if request.user.is_authenticated:
            user = Candidate.objects.get(name=request.user.username)
            form_2 = AddSkillForm
            extra = Skill.objects.exclude(candidate__id=user.id)
            my_list = list(set([i.tag.name for i in extra]))
            return render(request, 'account.html', {'user': user, 'mylist': my_list, 'form2': form_2, 'extra': extra})
        else:
            redirect('/login')


def register_user(request):
    """Регистрация кандидата"""
    if request.method == 'POST':
        new_form = RegistrationForm(request.POST)
        if new_form.is_valid():
            user = new_form.save()
            new_form.get_context()
            name = new_form.cleaned_data.get('username')
            surname = new_form.cleaned_data.get('last_name')
            lastname = new_form.cleaned_data.get('first_name')
            Candidate.objects.create(name=name, surname=surname, lastname=lastname)
            login(request, user)
            return redirect('/main')
        else:
            message = 'Не соблюдены все условия заполнения формы'
            return HttpResponse(message)

    else:
        form = RegistrationForm
    return render(request, 'register.html', {'form': form})


class UserLoginView(LoginView):
    """авторизация кандидата"""

    template_name = 'auth.html'
    next_page = '/main'


class Logout(LogoutView):
    """выход из учетной записи кандидата"""
    next_page = '/main'
