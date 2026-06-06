from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .forms import AppointmentForm, LoginForm, RegisterForm
from .models import Appointment, Workout


def is_fittime_admin(user):
    return user.is_authenticated and (user.username == 'Admin' or user.is_superuser)


def client_info(user):
    try:
        profile = user.profile
    except ObjectDoesNotExist:
        profile = None

    return {
        'name': profile.name if profile else (user.get_full_name() or user.username),
        'phone': profile.phone if profile else 'не указан',
        'email': user.email or 'не указан',
    }


class AppLoginView(LoginView):
    template_name = 'gym/login.html'
    authentication_form = LoginForm

    def get_success_url(self):
        if is_fittime_admin(self.request.user):
            return reverse_lazy('admin_panel')
        return reverse_lazy('workouts')


def home(request):
    return render(request, 'gym/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('workouts')
    else:
        form = RegisterForm()
    return render(request, 'gym/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def workouts(request):
    items = Workout.objects.all()
    return render(request, 'gym/workouts.html', {'workouts': items})


@login_required
def make_appointment(request, workout_id=None):
    initial = {}
    if workout_id:
        initial['workout'] = get_object_or_404(Workout, id=workout_id, is_available=True)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.status = Appointment.Status.NEW
            appointment.save()
            messages.success(request, 'Запись создана и отправлена администратору.')
            return redirect('cabinet')
    else:
        form = AppointmentForm(initial=initial)
    return render(request, 'gym/appointment_form.html', {'form': form})


@login_required
def cabinet(request):
    appointments = Appointment.objects.filter(client=request.user).select_related('workout')
    return render(request, 'gym/cabinet.html', {'appointments': appointments})


@login_required
def admin_panel(request):
    if not is_fittime_admin(request.user):
        messages.error(request, 'Доступ только для администратора.')
        return redirect('workouts')

    appointments = Appointment.objects.select_related('client', 'workout')
    rows = []
    for appointment in appointments:
        rows.append({
            'appointment': appointment,
            'client': client_info(appointment.client),
        })

    return render(request, 'gym/admin_panel.html', {
        'rows': rows,
        'statuses': Appointment.Status.choices,
    })


@require_POST
@login_required
def change_status(request, appointment_id):
    if not is_fittime_admin(request.user):
        messages.error(request, 'Недостаточно прав.')
        return redirect('workouts')
    appointment = get_object_or_404(Appointment, id=appointment_id)
    new_status = request.POST.get('status')
    allowed = [value for value, title in Appointment.Status.choices]
    if new_status in allowed:
        appointment.status = new_status
        appointment.save(update_fields=['status'])
        messages.success(request, 'Статус обновлен.')
    else:
        messages.error(request, 'Неверный статус.')
    return redirect('admin_panel')
