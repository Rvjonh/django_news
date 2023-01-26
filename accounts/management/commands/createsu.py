from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

import os


class Command(BaseCommand):
    help = "Creates a superuser."

    def handle(self, *args, **options):
        if not User.objects.filter(username=os.getenv("SUPER_USER_NAME")).exists():
            User.objects.create_superuser(
                username=os.getenv("SUPER_USER_NAME"),
                password=os.getenv("SUPER_USER_PASSWORD"),
            )
        print("Superuser has been created.")
