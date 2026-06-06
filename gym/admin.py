from django.contrib import admin

from .models import Appointment, Profile, Review, Workout


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'user')


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'duration_minutes', 'is_available')
    list_filter = ('is_available',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'workout', 'visit_datetime', 'visit_type', 'status')
    list_filter = ('status', 'visit_type')
    search_fields = ('client__username', 'client__profile__name', 'workout__title')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client', 'workout', 'rating', 'created_at')
