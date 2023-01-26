from django.core.management.base import BaseCommand

import os
from accounts.models import CustomUser


class Command(BaseCommand):
    help = "Creates a superuser."

    def handle(self, *args, **options):
        if not CustomUser.objects.filter(
            username=os.getenv("SUPER_USER_NAME")
        ).exists():
            CustomUser.objects.create_superuser(
                username=os.getenv("SUPER_USER_NAME"),
                password=os.getenv("SUPER_USER_PASSWORD"),
            )
        print("Superuser has been created.")
