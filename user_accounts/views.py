from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, customer_required, salon_owner_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import User, CustomerProfile, SalonOwnerProfile
from .forms import CustomerRegistrationForm, SalonOwnerRegistrationForm, UserLoginForm, UserProfileForm, CustomerProfileForm, SalonOwnerProfileForm, AdminUserCreationForm
from salon_management.models import Salon, Service, Staff, SalonHours
from booking_system.models import Booking, Review, Notification, Payment

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        # Redirect to appropriate dashboard based on user type
        if request.user.is_customer:
            return redirect('customer:dashboard')
        elif request.user.is_salon_owner:
            return redirect('salon_owner:dashboard')
        elif request.user.is_admin:
            return redirect('user_admin:dashboard')
        else:
            return redirect('core:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Try to authenticate with email as username
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.email}!')
                # Redirect to appropriate dashboard based on user type
                if user.is_customer:
                    return redirect('customer:dashboard')
                elif user.is_salon_owner:
                    return redirect('salon_owner:dashboard')
                elif user.is_admin:
                    return redirect('user_admin:dashboard')
                else:
                    return redirect('core:home')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    
    response = render(request, 'user_accounts/login.html', {'form': form})
    # Add cache control headers
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def admin_login_view(request):
    """Admin login view - separate from regular user login"""
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('user_admin:dashboard')
        else:
            messages.error(request, 'Access denied. This is the admin login portal.')
            return redirect('core:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Try to authenticate with email as username
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # Check if user is admin
                if user.is_admin:
                    login(request, user)
                    messages.success(request, f'Welcome to Admin Panel, {user.first_name or user.email}!')
                    return redirect('user_admin:dashboard')
                else:
                    messages.error(request, 'Access denied. Only administrators can access this portal.')
            else:
                messages.error(request, 'Invalid admin credentials. Please check your email and password.')
        else:
            # Handle form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.replace("_", " ").title()}: {error}')
    else:
        form = UserLoginForm()
    
    response = render(request, 'user_accounts/admin_login.html', {'form': form})
    # Add cache control headers
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    
    # Create response with cache control headers
    response = redirect('core:home')
    
    # Prevent caching of the logout page and subsequent pages
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

def customer_register_view(request):
    """Customer registration view"""
    if request.user.is_authenticated:
        # Redirect to appropriate dashboard based on user type
        if request.user.is_customer:
            return redirect('customer:dashboard')
        elif request.user.is_salon_owner:
            return redirect('salon_owner:dashboard')
        elif request.user.is_admin:
            return redirect('user_admin:dashboard')
        else:
            return redirect('core:home')
    
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Customer account created successfully! Welcome to BookMyStyle!')
            return redirect('customer:dashboard')
    else:
        form = CustomerRegistrationForm()
    
    response = render(request, 'user_accounts/customer_register.html', {'form': form})
    # Add cache control headers
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def salon_owner_register_view(request):
    """Salon owner registration view"""
    if request.user.is_authenticated:
        # Redirect to appropriate dashboard based on user type
        if request.user.is_customer:
            return redirect('customer:dashboard')
        elif request.user.is_salon_owner:
            return redirect('salon_owner:dashboard')
        elif request.user.is_admin:
            return redirect('user_admin:dashboard')
        else:
            return redirect('core:home')
    
    if request.method == 'POST':
        form = SalonOwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Salon owner account created successfully! Welcome to BookMyStyle!')
            return redirect('salon_owner:dashboard')
    else:
        form = SalonOwnerRegistrationForm()
    
    response = render(request, 'user_accounts/salon_owner_register.html', {'form': form})
    # Add cache control headers
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def register_choice_view(request):
    """Registration choice view"""
    if request.user.is_authenticated:
        # Redirect to appropriate dashboard based on user type
        if request.user.is_customer:
            return redirect('customer:dashboard')
        elif request.user.is_salon_owner:
            return redirect('salon_owner:dashboard')
        elif request.user.is_admin:
            return redirect('user_admin:dashboard')
        else:
            return redirect('core:home')
    
    response = render(request, 'user_accounts/register_choice.html')
    # Add cache control headers
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required
def profile_view(request):
    """User profile view"""
    user = request.user
    context = {
        'user': user,
    }
    
    if user.is_customer and hasattr(user, 'customer_profile'):
        context['customer_profile'] = user.customer_profile
    elif user.is_salon_owner and hasattr(user, 'salon_owner_profile'):
        context['salon_owner_profile'] = user.salon_owner_profile
    
    return render(request, 'user_accounts/profile.html', context)

@login_required
def edit_profile_view(request):
    """Edit user profile view"""
    user = request.user
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user)
    
    context = {
        'form': form,
        'user': user,
    }
    
    return render(request, 'user_accounts/edit_profile.html', context)

# Customer Views
@customer_required
def customer_dashboard(request):
    """Customer dashboard view"""
    
    user = request.user
    upcoming_bookings = Booking.objects.filter(
        customer=user,
        appointment_date__gte=timezone.now().date(),
        status__in=['pending', 'confirmed']
    ).order_by('appointment_date', 'appointment_time')[:5]
    
    recent_bookings = Booking.objects.filter(
        customer=user
    ).order_by('-created_at')[:5]
    
    context = {
        'upcoming_bookings': upcoming_bookings,
        'recent_bookings': recent_bookings,
        'total_bookings': Booking.objects.filter(customer=user).count(),
        'pending_bookings': Booking.objects.filter(customer=user, status='pending').count(),
    }
    
    return render(request, 'user_accounts/customer/dashboard.html', context)

@customer_required
def customer_bookings(request):
    """Customer bookings list view"""
    
    bookings = Booking.objects.filter(customer=request.user).order_by('-appointment_date', '-appointment_time')
    
    context = {
        'bookings': bookings,
    }
    
    return render(request, 'user_accounts/customer/bookings.html', context)

@customer_required
def booking_detail(request, booking_id):
    """Booking detail view"""
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'user_accounts/customer/booking_detail.html', context)

@customer_required
def cancel_booking(request, booking_id):
    """Cancel booking view"""
    
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('customer:bookings')
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'user_accounts/customer/cancel_booking.html', context)

@customer_required
def customer_reviews(request):
    """Customer reviews view"""
    
    reviews = Review.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {
        'reviews': reviews,
    }
    
    return render(request, 'user_accounts/customer/reviews.html', context)

@customer_required
def customer_notifications(request):
    """Customer notifications view"""
    
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark notifications as read
    notifications.update(is_read=True)
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, 'user_accounts/customer/notifications.html', context)

# Salon Owner Views
@salon_owner_required
def salon_owner_dashboard(request):
    """Salon owner dashboard view"""
    
    user = request.user
    salons = Salon.objects.filter(owner=user)
    
    # Get statistics
    total_bookings = Booking.objects.filter(salon__owner=user).count()
    pending_bookings = Booking.objects.filter(salon__owner=user, status='pending').count()
    today_bookings = Booking.objects.filter(
        salon__owner=user,
        appointment_date=timezone.now().date()
    ).count()
    
    recent_bookings = Booking.objects.filter(
        salon__owner=user
    ).order_by('-created_at')[:5]
    
    context = {
        'salons': salons,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'today_bookings': today_bookings,
        'recent_bookings': recent_bookings,
    }
    
    return render(request, 'user_accounts/salon_owner/dashboard.html', context)

@salon_owner_required
def salon_owner_salons(request):
    """Salon owner salons list view"""
    
    salons = Salon.objects.filter(owner=request.user).order_by('-created_at')
    
    context = {
        'salons': salons,
    }
    
    return render(request, 'user_accounts/salon_owner/salons.html', context)

@salon_owner_required
def create_salon(request):
    """Create salon view"""
    
    from salon_management.forms import SalonForm
    
    if request.method == 'POST':
        form = SalonForm(request.POST, request.FILES)
        if form.is_valid():
            salon = form.save(commit=False)
            salon.owner = request.user
            salon.save()
            messages.success(request, 'Salon created successfully! It will be reviewed by our admin team.')
            return redirect('salon_owner:salons')
    else:
        form = SalonForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'user_accounts/salon_owner/create_salon.html', context)

@salon_owner_required
def edit_salon(request, salon_id):
    """Edit salon view"""
    
    salon = get_object_or_404(Salon, id=salon_id, owner=request.user)
    
    # This would need a SalonForm - for now, just redirect
    messages.info(request, 'Salon editing form will be implemented soon.')
    return redirect('salon_owner:salons')

@salon_owner_required
def salon_owner_bookings(request):
    """Salon owner bookings view"""
    
    bookings = Booking.objects.filter(salon__owner=request.user).order_by('-appointment_date', '-appointment_time')
    
    context = {
        'bookings': bookings,
    }
    
    return render(request, 'user_accounts/salon_owner/bookings.html', context)

@salon_owner_required
def approve_booking(request, booking_id):
    """Approve booking view"""
    
    booking = get_object_or_404(Booking, id=booking_id, salon__owner=request.user)
    
    if request.method == 'POST':
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, 'Booking approved successfully.')
        return redirect('salon_owner:bookings')
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'user_accounts/salon_owner/approve_booking.html', context)

@salon_owner_required
def manage_staff(request):
    """Manage staff view"""
    
    # This would need staff management forms - for now, just show message
    messages.info(request, 'Staff management will be implemented soon.')
    return redirect('salon_owner:dashboard')

@salon_owner_required
def salon_analytics(request):
    """Salon analytics view"""
    
    # This would show analytics - for now, just show message
    messages.info(request, 'Analytics dashboard will be implemented soon.')
    return redirect('salon_owner:dashboard')

# Admin Views
@admin_required
def admin_dashboard(request):
    """Admin dashboard view"""
    
    # Get statistics
    total_users = User.objects.count()
    total_salons = Salon.objects.count()
    pending_salons = Salon.objects.filter(status='pending').count()
    total_bookings = Booking.objects.count()
    
    recent_salons = Salon.objects.filter(status='pending').order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'total_salons': total_salons,
        'pending_salons': pending_salons,
        'total_bookings': total_bookings,
        'recent_salons': recent_salons,
        'recent_users': recent_users,
    }
    
    return render(request, 'user_accounts/admin/dashboard.html', context)

@admin_required
def manage_users(request):
    """Manage users view"""
    
    users = User.objects.all().order_by('-date_joined')
    
    context = {
        'users': users,
    }
    
    return render(request, 'user_accounts/admin/users.html', context)

@admin_required
def create_user(request):
    """Create user view for admins"""
    
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully with role: {user.get_role_display()}')
            return redirect('user_admin:users')
    else:
        form = AdminUserCreationForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'user_accounts/admin/create_user.html', context)

@admin_required
def toggle_user_status(request, user_id):
    """Toggle user active status"""
    
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'User {user.username} has been {status}.')
    
    return redirect('user_admin:users')

@admin_required
def manage_salons(request):
    """Manage salons view"""
    
    salons = Salon.objects.all().order_by('-created_at')
    
    context = {
        'salons': salons,
    }
    
    return render(request, 'user_accounts/admin/salons.html', context)

@admin_required
def approve_salon(request, salon_id):
    """Approve salon"""
    
    salon = get_object_or_404(Salon, id=salon_id)
    salon.status = 'approved'
    salon.save()
    
    messages.success(request, f'Salon {salon.name} has been approved.')
    return redirect('user_admin:salons')

@admin_required
def reject_salon(request, salon_id):
    """Reject salon"""
    
    salon = get_object_or_404(Salon, id=salon_id)
    salon.status = 'rejected'
    salon.save()
    
    messages.success(request, f'Salon {salon.name} has been rejected.')
    return redirect('user_admin:salons')

@admin_required
def admin_bookings(request):
    """Admin bookings view"""
    
    bookings = Booking.objects.all().order_by('-created_at')
    
    context = {
        'bookings': bookings,
    }
    
    return render(request, 'user_accounts/admin/bookings.html', context)

@admin_required
def admin_analytics(request):
    """Admin analytics view"""
    
    # This would show platform analytics - for now, just show message
    messages.info(request, 'Analytics dashboard will be implemented soon.')
    return redirect('user_admin:dashboard')

@admin_required
def admin_settings(request):
    """Admin settings view"""
    
    # This would show site settings - for now, just show message
    messages.info(request, 'Settings management will be implemented soon.')
    return redirect('user_admin:dashboard')
