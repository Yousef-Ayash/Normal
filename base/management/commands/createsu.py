import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    help = "Creates a superuser."

    def handle(self, *args, **options):
        if not User.objects.filter(username=os.getenv("SUPERUSER")).exists():
            User.objects.create_superuser(
                username=os.getenv("SUPERUSER"), password=os.getenv("SUPERUSER_PASS")
            )
        print("Superuser has been created.")
