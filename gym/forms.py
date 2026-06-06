import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Appointment, Profile


class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин', min_length=6)
    password = forms.CharField(label='Пароль', min_length=8, widget=forms.PasswordInput)
    name = forms.CharField(label='Имя')
    phone = forms.CharField(label='Телефон', help_text='8 (XXX) XXX-XX-XX')
    email = forms.EmailField(label='Email')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.fullmatch(r'[A-Za-z0-9]{6,}', username):
            raise forms.ValidationError('Логин должен быть от 6 символов, только латиница и цифры.')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Такой логин уже занят.')
        return username

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.fullmatch(r'[А-Яа-яЁё\-\s]+', name):
            raise forms.ValidationError('Имя должно быть на кириллице.')
        return name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.fullmatch(r'8 \(\d{3}\) \d{3}-\d{2}-\d{2}', phone):
            raise forms.ValidationError('Телефон должен быть в формате 8 (XXX) XXX-XX-XX.')
        return phone

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
        )
        Profile.objects.create(user=user, name=self.cleaned_data['name'], phone=self.cleaned_data['phone'])
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    error_messages = {
        'invalid_login': 'Некорректный логин или пароль.',
        'inactive': 'Пользователь не активен.',
    }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['workout', 'visit_datetime', 'visit_type', 'comment']
        widgets = {
            'visit_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_visit_datetime(self):
        visit_datetime = self.cleaned_data['visit_datetime']
        if visit_datetime <= timezone.now():
            raise forms.ValidationError('Нельзя записаться на прошедшую дату и время.')
        return visit_datetime
