from django.core.management.base import BaseCommand
from bank_app.consumer import start_consuming

class Command(BaseCommand):
    help = 'Consume messages from the RabbitMQ queue'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting RabbitMQ consumer...'))
        start_consuming()
