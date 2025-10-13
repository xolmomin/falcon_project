from datetime import timezone
from random import choice

from django.core.management.base import BaseCommand
from faker import Faker

from apps.factories import CategoryFactory
from apps.models import Category, Tag, User


class Command(BaseCommand):
    help = "Malumot qoshish"

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        self.faker = Faker()
        self.names = {'category', 'product', 'user', 'tag'}
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        parser.add_argument("--category", type=int)
        parser.add_argument("--product", type=int)
        parser.add_argument("--user", type=int)
        parser.add_argument("--tag", type=int)
        parser.add_argument("--all", type=int)

    def generate_category(self, count: int):  # 5000
        CategoryFactory.create_batch(count)
        # category_list = []
        # for _ in range(count):
        #     category_list.append(Category(name=self.faker.company()))
        #
        # Category.objects.bulk_create(category_list, batch_size=500)

    def generate_product(self):
        pass

    def generate_user(self, count: int):
        for _ in range(count):
            _username = self.faker.user_name()
            while User.objects.filter(username=_username).exists():
                _username = self.faker.user_name()

            User.objects.create_user(
                username=_username,
                email=self.faker.email(domain='gmail.com'),
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                type=choice(User.Type.choices)[0],
                date_joined=self.faker.date_time(tzinfo=timezone.utc),
            )

    def generate_tag(self, count: int):
        for _ in range(count):
            Tag.objects.create(name=self.faker.company())

    def handle(self, *args, **options):
        for item in set(options).intersection(self.names):
            if count := options.get(item):
                getattr(self, f'generate_{item}')(count)
                self.stdout.write(self.style.SUCCESS(f'Successfully added {count} {item}'))
