from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

username = "admini"


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=f"{username}@example.com", password="Password")
            self.stdout.write(self.style.SUCCESS("スーパーユーザの作成に成功"))
