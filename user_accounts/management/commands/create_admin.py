from django.core.management.base import BaseCommand
from user_accounts.models import User


class Command(BaseCommand):
    help = 'Create an admin user for testing'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Admin email', default='admin@bookmystyle.com')
        parser.add_argument('--password', type=str, help='Admin password', default='admin123')
        parser.add_argument('--first-name', type=str, help='Admin first name', default='Admin')
        parser.add_argument('--last-name', type=str, help='Admin last name', default='User')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']

        # Show existing admin users
        existing_superusers = User.objects.filter(is_superuser=True)
        existing_admins = User.objects.filter(role='admin')
        
        if existing_superusers.exists() or existing_admins.exists():
            self.stdout.write(self.style.SUCCESS('Existing admin access accounts:'))
            for su in existing_superusers:
                self.stdout.write(f'  Superuser: {su.email} (username: {su.username})')
            for admin in existing_admins:
                self.stdout.write(f'  Admin role: {admin.email}')
            self.stdout.write('')

        # Check if admin user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin user with email {email} already exists')
            )
            return

        # Create admin user
        admin_user = User.objects.create_user(
            username=email,  # Use email as username
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='admin',
            is_active=True,
            is_staff=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created admin user:\n'
                f'Email: {email}\n'
                f'Password: {password}\n'
                f'Name: {first_name} {last_name}\n'
                f'You can now login at /accounts/admin_portal/'
            )
        )