import random
from decimal import Decimal

from django.core.management.base import BaseCommand

from accounts.models import Profile
from store.models import Product, Category


class Command(BaseCommand):

    help = "Create demo marketplace products"

    def add_arguments(self, parser):

        parser.add_argument(
            '--count',
            type=int,
            default=500,
            help='Number of products to create'
        )


    def handle(self, *args, **options):

        count = options['count']


        # =====================================
        # SELLERS
        # =====================================

        seller_profiles = Profile.objects.filter(
            role='seller'
        ).select_related('user')

        sellers = [
            profile.user
            for profile in seller_profiles
        ]

        if not sellers:

            self.stdout.write(
                self.style.ERROR(
                    'No seller account found.'
                )
            )
            return


        # =====================================
        # CATEGORIES + BRANDS
        # =====================================

        category_data = {

            'Electronics': [
                'Samsung',
                'Apple',
                'Xiaomi',
                'Realme',
                'OnePlus'
            ],

            'Computers': [
                'HP',
                'Dell',
                'Lenovo',
                'Asus',
                'Acer'
            ],

            'Fashion': [
                'Nike',
                'Adidas',
                'Puma',
                'Zara',
                'H&M'
            ],

            'Home & Living': [
                'Walton',
                'Vision',
                'Singer',
                'Minister',
                'RFL'
            ],

            'Beauty': [
                'Nivea',
                'Dove',
                'Garnier',
                'Loreal',
                'Vaseline'
            ],

            'Sports': [
                'Nike',
                'Adidas',
                'Puma',
                'Reebok',
                'Wilson'
            ],

            'Accessories': [
                'Baseus',
                'Hoco',
                'Anker',
                'Oraimo',
                'Remax'
            ],

            'Groceries': [
                'Pran',
                'ACI',
                'Fresh',
                'Radhuni',
                'Nestle'
            ],
        }


        product_types = {

            'Electronics': [
                'Smartphone',
                'Smart Watch',
                'Bluetooth Speaker',
                'Earbuds',
                'Power Bank',
                'Tablet',
                'Headphone'
            ],

            'Computers': [
                'Laptop',
                'Keyboard',
                'Mouse',
                'Monitor',
                'SSD',
                'RAM',
                'Laptop Stand'
            ],

            'Fashion': [
                'T-Shirt',
                'Shirt',
                'Jeans',
                'Sneakers',
                'Jacket',
                'Hoodie',
                'Polo Shirt'
            ],

            'Home & Living': [
                'Fan',
                'Rice Cooker',
                'Blender',
                'Iron',
                'Electric Kettle',
                'Table Lamp'
            ],

            'Beauty': [
                'Face Wash',
                'Body Lotion',
                'Shampoo',
                'Perfume',
                'Cream'
            ],

            'Sports': [
                'Football',
                'Cricket Bat',
                'Sports Shoes',
                'Gym Bag',
                'Yoga Mat'
            ],

            'Accessories': [
                'USB Cable',
                'Charger',
                'Phone Case',
                'Backpack',
                'Wallet'
            ],

            'Groceries': [
                'Rice',
                'Oil',
                'Biscuits',
                'Noodles',
                'Coffee',
                'Tea'
            ],
        }


        # =====================================
        # CREATE CATEGORIES
        # =====================================

        categories = {}

        for category_name in category_data:

            category, created = Category.objects.get_or_create(
                name=category_name
            )

            categories[category_name] = category


        # =====================================
        # CREATE PRODUCTS
        # =====================================

        products = []

        start_number = Product.objects.count() + 1


        for number in range(
            start_number,
            start_number + count
        ):

            category_name = random.choice(
                list(category_data.keys())
            )

            category = categories[
                category_name
            ]

            brand = random.choice(
                category_data[
                    category_name
                ]
            )

            product_type = random.choice(
                product_types[
                    category_name
                ]
            )

            seller = random.choice(
                sellers
            )

            price = Decimal(
                str(
                    random.randint(
                        200,
                        100000
                    )
                )
            )

            stock = random.randint(
                5,
                200
            )

            product_name = (
                f'{brand} {product_type} '
                f'Model {number}'
            )


            products.append(

                Product(
                    seller=seller,
                    category=category,
                    name=product_name,
                    brand=brand,
                    description=(
                        f'High quality {brand} '
                        f'{product_type}. '
                        f'Demo marketplace product.'
                    ),
                    price=price,
                    stock=stock,
                    is_active=True
                )
            )


            # Insert every 1000 products
            if len(products) >= 1000:

                Product.objects.bulk_create(
                    products,
                    batch_size=1000
                )

                products = []


        # Remaining products
        if products:

            Product.objects.bulk_create(
                products,
                batch_size=1000
            )


        self.stdout.write(
            self.style.SUCCESS(
                f'{count} products created successfully!'
            )
        )