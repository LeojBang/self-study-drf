from django.core.management import BaseCommand

from authentication.models import User


class Command(BaseCommand):
    """Команда для создания администратора"""

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email="admin@example.com", first_name="Admin", role="admin"
        )
        user.set_password("12345")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
