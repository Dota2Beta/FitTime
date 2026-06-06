from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.AppLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('workouts/', views.workouts, name='workouts'),
    path('appointment/', views.make_appointment, name='appointment'),
    path('appointment/<int:workout_id>/', views.make_appointment, name='appointment_for_workout'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/status/<int:appointment_id>/', views.change_status, name='change_status'),
]
