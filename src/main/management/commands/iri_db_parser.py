from django.core.management import BaseCommand

from main.models import Task
from main.modules.parser import parser


class Command(BaseCommand):
    help = "Runs consumer."

    def handle(self, *args, **options):
        print("started")
        parser()
