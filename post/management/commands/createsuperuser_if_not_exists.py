"""
Django management command to create a superuser if one doesn't exist.
Reads SUPER_ADMIN_ACCOUNT and SUPER_ADMIN_PASSWORD from environment variables.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser if one doesn't exist using environment variables"

    def handle(self, *args, **options):
        User = get_user_model()

        # Get environment variables
        admin_account = os.getenv("SUPER_ADMIN_ACCOUNT")
        admin_password = os.getenv("SUPER_ADMIN_PASSWORD")

        if not admin_account:
            self.stdout.write(
                self.style.WARNING(
                    "SUPER_ADMIN_ACCOUNT environment variable is not set. Skipping superuser creation."
                )
            )
            return

        if not admin_password:
            self.stdout.write(
                self.style.WARNING(
                    "SUPER_ADMIN_PASSWORD environment variable is not set. Skipping superuser creation."
                )
            )
            return

        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.SUCCESS("A superuser already exists. Skipping creation.")
            )
            return

        # Check if user with this username already exists
        if User.objects.filter(username=admin_account).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"User '{admin_account}' already exists but is not a superuser. "
                    "Skipping creation."
                )
            )
            return

        # Create superuser
        try:
            User.objects.create_superuser(
                username=admin_account,
                password=admin_password,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created superuser '{admin_account}'")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating superuser: {str(e)}"))
