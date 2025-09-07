from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('dashboard/', views.customer_dashboard, name='dashboard'),
    path('bookings/', views.customer_bookings, name='bookings'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('reviews/', views.customer_reviews, name='reviews'),
    path('notifications/', views.customer_notifications, name='notifications'),
]
