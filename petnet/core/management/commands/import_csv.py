import csv
from django.core.management.base import BaseCommand
from store.models import Product  # Import your model here

class Command(BaseCommand):
    help = 'Import data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product = Product(
                    name=row['name'],
                    voucherDefinition=row['voucherDefinition'],
                    IssuedDate=row['IssuedDate'],
                    price=row['price'],
                    totalAmount=row['totalAmount'],
                    Category=row['Category'],
                    grandTotal=row['grandTotal'],
                    consignee=row['consignee'],
                    User=row['User'],
                    Group=row['Group'],
                    Order=row['Order'],
                    OrderItem=row['OrderItem'],
                    Userprofile=row['Userprofile'],
                )
                product.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {product.name}'))
