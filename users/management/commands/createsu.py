from django.core.management.base import BaseCommand
from users.models import User

# AWS 배포할때 수퍼 유저 생성
class Command(BaseCommand):

    help = "This command creates superuser"

    def handle(self, *args, **options):

        if User.objects.filter(username="djadmin"):
            self.stdout.write(self.style.SUCCESS(f"Superuser Exists"))
        else:
            User.objects.create_superuser(
                "djadmin", "park.awstudy@gmail.com", "djadmin"
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser Created"))
