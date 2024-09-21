from django.core.management.base import BaseCommand
from extra_scripts.db_fake_data_fill import main


class Command(BaseCommand):
    help = 'Заполняет базу данных, тестовыми данными'

    def handle(self, *args, **kwargs):
        self.stdout.write("Заполняем базу данных...")
        main()
