from bets.database import load_matches
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Loads matches from football-data API'

    def handle(self, **options):
        load_matches()
