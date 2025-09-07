from django.urls import path
from . import views

app_name = 'salon_owner'

urlpatterns = [
    path('dashboard/', views.salon_owner_dashboard, name='dashboard'),
    path('salons/', views.salon_owner_salons, name='salons'),
    path('salons/create/', views.create_salon, name='create_salon'),
    path('salons/<int:salon_id>/edit/', views.edit_salon, name='edit_salon'),
    path('bookings/', views.salon_owner_bookings, name='bookings'),
    path('bookings/<int:booking_id>/approve/', views.approve_booking, name='approve_booking'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('staff/', views.manage_staff, name='staff'),
    path('analytics/', views.salon_analytics, name='analytics'),
]
