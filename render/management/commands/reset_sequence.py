from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Resets the sequence of the specified table'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT setval(pg_get_serial_sequence('render_asahiyaki', 'id'), (SELECT MAX(id) FROM render_asahiyaki) + 1);
            """)
        self.stdout.write(self.style.SUCCESS('Sequence reset successfully'))
