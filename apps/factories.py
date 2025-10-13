from factory import LazyAttribute
from factory.django import DjangoModelFactory
from faker import Faker

from apps.models import Category

fake = Faker()


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = LazyAttribute(lambda _: fake.company())
