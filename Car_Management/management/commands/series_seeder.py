import csv
from django.core.management.base import BaseCommand
from Car_Management.models import CarSerie

class Command(BaseCommand):
    help = 'Import from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        total_rows = sum(1 for line in open(csv_file, encoding='utf-8'))  # Count total number of rows in CSV
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            processed_rows = 0
            for row in reader:
                carserie = CarSerie(
                    id=row['id'],
                    name=row['name'],
                    generation_id=row['generation_id'],
                    model_id=row['model_id']
                )
                carserie.save()
                processed_rows += 1
                self.stdout.write(f'\rProcessed: {processed_rows}/{total_rows}', ending='')

        self.stdout.write(self.style.SUCCESS('\nData imported successfully'))