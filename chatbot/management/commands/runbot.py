from django.core.management.base import BaseCommand, CommandError

from chatbot.utils import bot


class Command(BaseCommand):
    help = 'Run chatbot'

    def add_arguments(self, parser):
        #parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        try:
            bot.polling()
        except Exception as err:
            CommandError(str(err))
