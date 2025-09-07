from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, CustomerProfile, SalonOwnerProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('role', 'is_verified', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'profile_picture', 'date_of_birth', 'address', 'is_verified')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'profile_picture', 'date_of_birth', 'address', 'is_verified')}),
    )


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'loyalty_points', 'total_bookings')
    search_fields = ('user__username', 'user__email')
    filter_horizontal = ('preferred_services',)


@admin.register(SalonOwnerProfile)
class SalonOwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_license', 'years_of_experience', 'total_salons')
    search_fields = ('user__username', 'user__email', 'business_license')