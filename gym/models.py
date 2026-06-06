from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField('Имя', max_length=80)
    phone = models.CharField('Телефон', max_length=18)

    def __str__(self):
        return self.name


class Workout(models.Model):
    title = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    price = models.DecimalField('Стоимость', max_digits=8, decimal_places=2)
    duration_minutes = models.PositiveIntegerField('Длительность, минут')
    is_available = models.BooleanField('Доступна', default=True)

    def __str__(self):
        return self.title


class Appointment(models.Model):
    class VisitType(models.TextChoices):
        FIRST = 'first', 'Первичное'
        REPEAT = 'repeat', 'Повторное'

    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        CONFIRMED = 'confirmed', 'Подтверждена'
        CLIENT_CAME = 'client_came', 'Клиент посетил тренировку'
        DONE = 'done', 'Тренировка проведена'
        CANCELLED = 'cancelled', 'Отменена'

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    workout = models.ForeignKey(Workout, on_delete=models.PROTECT, related_name='appointments')
    visit_datetime = models.DateTimeField('Дата и время посещения')
    visit_type = models.CharField('Тип посещения', max_length=10, choices=VisitType.choices)
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField('Статус', max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField('Создана', auto_now_add=True)

    class Meta:
        ordering = ['-visit_datetime']

    def __str__(self):
        return f'{self.client.username} - {self.workout.title}'


class Review(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField('Текст отзыва')
    rating = models.PositiveSmallIntegerField('Оценка')
    created_at = models.DateTimeField('Дата отзыва', auto_now_add=True)

    def __str__(self):
        return f'Отзыв {self.client.username}: {self.rating}'
