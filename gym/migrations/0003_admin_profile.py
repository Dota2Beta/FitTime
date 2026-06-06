from django.db import migrations


def add_admin_profile(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('gym', 'Profile')

    admin = User.objects.filter(username='Admin').first()
    if admin:
        Profile.objects.get_or_create(
            user=admin,
            defaults={
                'name': 'Администратор',
                'phone': '8 (000) 000-00-00',
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ('gym', '0002_seed_data'),
    ]

    operations = [migrations.RunPython(add_admin_profile, migrations.RunPython.noop)]
