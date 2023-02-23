from django.core.management.base import BaseCommand
from Users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            User.objects.create_superuser("admin@jabotics.in", "Jab@2023", "Jabotics", "Jabotics")
        
        except:
            pass
        
        print("\n[+] Successfully added super admin")
        print("[*] Username: admin@jabotics.in")
        print("[*] Password: Jab@2023\n")