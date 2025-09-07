from django.urls import path
from . import views

app_name = 'user_admin'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('users/', views.manage_users, name='users'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    path('salons/', views.manage_salons, name='salons'),
    path('salons/<int:salon_id>/approve/', views.approve_salon, name='approve_salon'),
    path('salons/<int:salon_id>/reject/', views.reject_salon, name='reject_salon'),
    path('bookings/', views.admin_bookings, name='bookings'),
    path('analytics/', views.admin_analytics, name='analytics'),
    path('settings/', views.admin_settings, name='settings'),
]
