from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse, resolve
from django.utils.deprecation import MiddlewareMixin


class RoleBasedAccessMiddleware(MiddlewareMixin):
    """
    Middleware to enforce role-based access control at the URL level
    """
    
    # Define role-specific URL patterns
    ADMIN_ONLY_PATTERNS = [
        'user_admin:',
    ]
    
    CUSTOMER_ONLY_PATTERNS = [
        'customer:',
    ]
    
    SALON_OWNER_ONLY_PATTERNS = [
        'salon_owner:',
    ]
    
    def process_request(self, request):
        # Skip for unauthenticated users (let Django's login_required handle it)
        if not request.user.is_authenticated:
            return None
        
        # Get the current URL name
        try:
            current_url = resolve(request.path_info)
            url_name = f"{current_url.namespace}:{current_url.url_name}" if current_url.namespace else current_url.url_name
        except:
            return None
        
        user = request.user
        
        # Check admin-only patterns
        for pattern in self.ADMIN_ONLY_PATTERNS:
            if url_name and url_name.startswith(pattern):
                if not user.is_admin:
                    messages.error(request, 'Access denied. Admin privileges required.')
                    return self._redirect_to_user_dashboard(user)
        
        # Check customer-only patterns
        for pattern in self.CUSTOMER_ONLY_PATTERNS:
            if url_name and url_name.startswith(pattern):
                if not user.is_customer:
                    messages.error(request, 'Access denied. Customer account required.')
                    return self._redirect_to_user_dashboard(user)
        
        # Check salon owner-only patterns
        for pattern in self.SALON_OWNER_ONLY_PATTERNS:
            if url_name and url_name.startswith(pattern):
                if not user.is_salon_owner:
                    messages.error(request, 'Access denied. Salon owner account required.')
                    return self._redirect_to_user_dashboard(user)
        
        return None
    
    def _redirect_to_user_dashboard(self, user):
        """Redirect user to their appropriate dashboard"""
        if user.is_admin:
            return redirect('user_admin:dashboard')
        elif user.is_salon_owner:
            return redirect('salon_owner:dashboard')
        elif user.is_customer:
            return redirect('customer:dashboard')
        else:
            return redirect('core:home')


class NoCacheMiddleware(MiddlewareMixin):
    """
    Middleware to prevent caching of sensitive pages
    """
    
    SENSITIVE_PATTERNS = [
        'accounts:',
        'user_admin:',
        'customer:',
        'salon_owner:',
    ]
    
    def process_response(self, request, response):
        # Check if current URL should not be cached
        try:
            current_url = resolve(request.path_info)
            url_name = f"{current_url.namespace}:{current_url.url_name}" if current_url.namespace else current_url.url_name
            
            for pattern in self.SENSITIVE_PATTERNS:
                if url_name and url_name.startswith(pattern):
                    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
                    response['Pragma'] = 'no-cache'
                    response['Expires'] = '0'
                    break
        except:
            pass
        
        return response


class SessionSecurityMiddleware(MiddlewareMixin):
    """
    Middleware for additional session security
    """
    
    def process_request(self, request):
        if request.user.is_authenticated:
            # Store user role in session for additional verification
            current_role = None
            if request.user.is_admin:
                current_role = 'admin'
            elif request.user.is_salon_owner:
                current_role = 'salon_owner'
            elif request.user.is_customer:
                current_role = 'customer'
            
            # Check if role changed (security measure)
            session_role = request.session.get('user_role')
            if session_role and session_role != current_role:
                # Role mismatch - possible security issue
                messages.warning(request, 'Session security check failed. Please log in again.')
                from django.contrib.auth import logout
                logout(request)
                return redirect('accounts:login')
            
            # Update session with current role
            request.session['user_role'] = current_role
        
        return None