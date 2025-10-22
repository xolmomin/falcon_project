import os
from datetime import timedelta

from PIL import ImageOps, Image
from django.db.models import Model, CharField, PositiveSmallIntegerField, PositiveIntegerField, \
    ForeignKey, CASCADE, Q, ManyToManyField, ImageField, OneToOneRel, OneToOneField
from django.db.models.constraints import CheckConstraint
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from django_jsonform.models.fields import JSONField

from apps.models import users
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

    name = CharField(verbose_name=_('Name'), max_length=255)
    price = PositiveIntegerField(verbose_name=_('Price'))
    discount_percentage = PositiveSmallIntegerField(default=0, db_default=0,
                                                    help_text="Discount percentage must be between 0 and 100")
    short_description = CKEditor5Field(blank=True)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    tags = ManyToManyField('apps.Tag', blank=True)
    description = CKEditor5Field(blank=True)
    specification = JSONField(schema=ITEMS_SCHEMA, blank=True)
    shipping_cost = PositiveSmallIntegerField(verbose_name=_('Shipping cost'))
    quantity = PositiveIntegerField(verbose_name=_('Count'), default=0, db_default=0)
    like_count = PositiveIntegerField(default=0, db_default=0, editable=False)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = '-created_at',

        constraints = [
            CheckConstraint(condition=Q(discount_percentage__gte=0) & Q(discount_percentage__lte=100),
                            name="discount_percentage_gte_0_lte_100",
                            violation_error_message="Discount percentage must be between 0 and 100")
        ]

    def __str__(self):
        return self.name

    @property
    def first_image(self):
        return self.images.first()

    @property
    def discount_price(self):
        return self.price - int(self.discount_percentage * self.price / 100)

    @property
    def is_new(self):
        return self.created_at > now() - timedelta(days=3)

    def delete(self, using=None, keep_parents=False):
        for product_image in self.images.all():
            product_image.delete()
        return super().delete(using, keep_parents)


class ProductImage(Model):
    image = ImageField(upload_to='products/%Y/%m/%d')
    product = ForeignKey('apps.Product', CASCADE, related_name='images')

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        img_path = self.image.path
        img = Image.open(img_path)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        target_size = (777, 508)
        img = ImageOps.fit(img, target_size, Image.Resampling.LANCZOS)

        webp_path = os.path.splitext(img_path)[0] + ".webp"
        img.save(webp_path, "WEBP", quality=90)

        if img_path != webp_path and os.path.exists(img_path):
            os.remove(img_path)

        self.image.name = os.path.splitext(self.image.name)[0] + ".webp"
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=["image"])

    def delete(self, using=None, keep_parents=False):
        self.image.delete(False)
        return super().delete(using, keep_parents)


class Cart(Model):
    user = OneToOneField('apps.User', CASCADE)


class CartItem(Model):
    cart = ForeignKey('apps.Cart', CASCADE, related_name='cart_items')
    product = ForeignKey('apps.Product', CASCADE, related_name='cart_items')
    quantity = PositiveIntegerField(verbose_name=_('Quantity'))
