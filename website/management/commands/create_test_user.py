from django.core.management.base import BaseCommand
from website.models.UserModel import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Create a test user for testing purposes'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='test', help='Username for the test user')
        parser.add_argument('--password', type=str, default='test', help='Password for the test user')
        parser.add_argument('--email', type=str, default='test@example.com', help='Email for the test user')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists!')
            )
            return
        
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'User with email "{email}" already exists!')
            )
            return
        
        # Create the test user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created test user "{username}" with password "{password}"')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Email: {email}')
        )
        self.stdout.write(
            self.style.SUCCESS('This user has no Author or Reader profile, perfect for testing the mobile menu!')
        )