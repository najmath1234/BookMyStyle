from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom User model with role-based authentication
    """
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('salon_owner', 'Salon Owner'),
        ('admin', 'Admin'),
    ]
    
    # Public registration choices (excludes admin)
    PUBLIC_ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('salon_owner', 'Salon Owner'),
    ]
    
    # Use email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    # Make email unique since it's the username field
    email = models.EmailField(unique=True)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")],
        blank=True,
        null=True
    )
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_customer(self):
        return self.role == 'customer'
    
    @property
    def is_salon_owner(self):
        return self.role == 'salon_owner'
    
    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser


class CustomerProfile(models.Model):
    """
    Extended profile for customers
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    preferred_services = models.ManyToManyField('salon_management.Service', blank=True)
    loyalty_points = models.IntegerField(default=0)
    total_bookings = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Customer Profile - {self.user.username}"


class SalonOwnerProfile(models.Model):
    """
    Extended profile for salon owners
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='salon_owner_profile')
    business_license = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.IntegerField(default=0)
    total_salons = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Salon Owner Profile - {self.user.username}"