from random import randrange

from django.core.management.base import BaseCommand
from faker import Faker

from ecommerce.models import Product


class Command(BaseCommand):
    help = 'Generate fake data product'
    product_suggestion_list = [
        'danish', 'cheesecake', 'sugar',
        'Lollipop', 'wafer', 'Gummies',
        'sesame', 'Jelly', 'beans',
        'pie', 'bar', 'Ice', 'oat'
    ]
    random_range_price = 1000000

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Indicates the number of products to be generate')

    def handle(self, *args, **kwargs):
        fake = Faker()
        num = kwargs.get('count')
        products = []

        for counter in range(num):
            price = randrange(Command.random_range_price)
            products.append(Product(
                name=fake.sentence(ext_word_list=Command.product_suggestion_list),
                price=price)
            )

        Product.objects.bulk_create(products)
        message = f'Successfully added {num} products'
        self.stdout.write("%s" % message)
