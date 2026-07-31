from django.contrib.auth.models import User
from django.core.management import BaseCommand
from accounts.models import Organization, UserProfile


class Command(BaseCommand):
    help = 'Add test users'

    def _create_admin_profile(self):
        org, _ = Organization.objects.get_or_create(name='Test Organization')
        admin_email = 'admin@garage360.com'
        if User.objects.filter(email=admin_email).exists():
            self.stdout.write(self.style.WARNING('Admin user already exists!'))
            return

        # Create the profile + user
        user_profile = UserProfile.objects.create_admin(
            organization=org,
            email=admin_email,
            first_name='AdminF',
            last_name='AdminL',
            phone_number='+49 555 555 555',
        )

        # set the password
        user_profile.set_password('rf$Awe1tg0900P1#')
        self.stdout.write(self.style.SUCCESS('Admin user added!'))

    def handle(self, *args, **options):
        self._create_admin_profile()

