from django.core.management.base import BaseCommand
from queue_ls.queue_listener import UserCheckout
class Command(BaseCommand):
    help = 'Launches Listener for user_created message : RaabitMQ'
    def handle(self, *args, **options):
        td = UserCheckout()
        td.start()
        self.stdout.write("Started Consumer Thread")