from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('admin_portal/', views.admin_login_view, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_choice_view, name='register'),
    path('register/customer/', views.customer_register_view, name='customer_register'),
    path('register/salon-owner/', views.salon_owner_register_view, name='salon_owner_register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
]
