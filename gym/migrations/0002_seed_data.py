from django.db import migrations


def seed(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Workout = apps.get_model('gym', 'Workout')

    if not User.objects.filter(username='Admin').exists():
        admin = User.objects.create_superuser(username='Admin', email='admin@fittime.local', password='FitTimeAdmin')
        admin.first_name = 'Администратор'
        admin.save(update_fields=['first_name'])

    workouts = [
        ('Силовая тренировка', 'Упражнения на основные группы мышц с тренером.', 900, 60, True),
        ('Йога', 'Спокойная тренировка для гибкости и дыхания.', 700, 50, True),
        ('Кардио', 'Интенсивная тренировка для выносливости.', 650, 45, True),
        ('Растяжка', 'Занятие для восстановления и подвижности.', 600, 40, True),
    ]
    for title, description, price, duration, available in workouts:
        Workout.objects.get_or_create(
            title=title,
            defaults={
                'description': description,
                'price': price,
                'duration_minutes': duration,
                'is_available': available,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0001_initial'),
    ]

    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
