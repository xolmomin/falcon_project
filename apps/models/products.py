from datetime import timedelta

from django.db.models import Model, CharField, PositiveSmallIntegerField, PositiveIntegerField, \
    TextField, ForeignKey, CASCADE, Q, ManyToManyField, ImageField
from django.db.models.constraints import CheckConstraint
from django.utils.timezone import now
from django_jsonform.models.fields import JSONField

from apps.models.base import SlugBaseModel, CreatedBaseModel


class Category(SlugBaseModel):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(SlugBaseModel):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(SlugBaseModel, CreatedBaseModel):
    ITEMS_SCHEMA = {
        'type': 'array',
        'items': {
            'type': 'object',
            'keys': {
                'name': {
                    'type': 'string'
                },
                'value': {
                    'type': 'string'
                }
            }
        },
        'default': [],
    }

    name = CharField(max_length=255)
    price = PositiveIntegerField()
    discount_percentage = PositiveSmallIntegerField(default=0, db_default=0,
                                                    help_text="Discount percentage must be between 0 and 100")
    short_description = TextField(blank=True)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    tags = ManyToManyField('apps.Tag', blank=True)
    description = TextField(blank=True)
    specification = JSONField(schema=ITEMS_SCHEMA, blank=True)
    shipping_cost = PositiveSmallIntegerField()
    quantity = PositiveIntegerField(default=0, db_default=0)
    like_count = PositiveIntegerField(default=0, db_default=0, editable=False)

    class Meta:
        constraints = [
            CheckConstraint(condition=Q(discount_percentage__gte=0) & Q(discount_percentage__lte=100),
                            name="discount_percentage_gte_0_lte_100",
                            violation_error_message="Discount percentage must be between 0 and 100")
        ]

    def __str__(self):
        return self.name

    @property
    def discount_price(self):
        return self.price - int(self.discount_percentage * self.price / 100)

    @property
    def is_new(self):
        return self.created_at > now() - timedelta(days=3)


class ProductImage(Model):
    image = ImageField(upload_to='products/%Y/%m/%d')
    product = ForeignKey('apps.Product', CASCADE, related_name='images')
