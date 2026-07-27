from django.contrib.auth.models import User
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Add test users'

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_user(
                username='admin',
                email='admin@localhost',
                password='rf$Awe1tg0900P1#',
            )
            self.stdout.write(self.style.SUCCESS('Admin user added!'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists!'))
