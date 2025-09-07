from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def role_required(*allowed_roles):
    """
    Decorator that checks if the user has the required role.
    
    Usage:
    @role_required('admin')
    @role_required('customer', 'salon_owner')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user = request.user
            
            # Check if user has any of the allowed roles
            user_roles = []
            if user.is_admin:
                user_roles.append('admin')
            if user.is_customer:
                user_roles.append('customer')
            if user.is_salon_owner:
                user_roles.append('salon_owner')
            
            # Check if user has any allowed role
            if any(role in user_roles for role in allowed_roles):
                return view_func(request, *args, **kwargs)
            
            # Redirect to appropriate dashboard with error message
            messages.error(request, 'Access denied. You do not have permission to access this page.')
            
            # Redirect to user's appropriate dashboard
            if user.is_admin:
                return redirect('user_admin:dashboard')
            elif user.is_salon_owner:
                return redirect('salon_owner:dashboard')
            elif user.is_customer:
                return redirect('customer:dashboard')
            else:
                return redirect('core:home')
        
        return wrapper
    return decorator


def admin_required(view_func):
    """Decorator for admin-only views"""
    return role_required('admin')(view_func)


def customer_required(view_func):
    """Decorator for customer-only views"""
    return role_required('customer')(view_func)


def salon_owner_required(view_func):
    """Decorator for salon owner-only views"""
    return role_required('salon_owner')(view_func)


def business_user_required(view_func):
    """Decorator for business users (admin or salon owner)"""
    return role_required('admin', 'salon_owner')(view_func)