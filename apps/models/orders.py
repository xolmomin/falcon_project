from django.db.models import CharField, PositiveIntegerField, \
    ForeignKey, CASCADE, TextChoices
from django.utils.translation import gettext_lazy as _

from apps.models.base import CreatedBaseModel


class Order(CreatedBaseModel):
    class Status(TextChoices):
        IN_PROGRESS = 'in_progress', 'In progress'
        PAID = 'paid', 'Paid'
        CANCELED = 'canceled', 'Canceled'

    user = ForeignKey('apps.User', CASCADE, related_name='orders')
    status = CharField(max_length=255, default=Status.IN_PROGRESS, choices=Status.choices)


class OrderItem(CreatedBaseModel):
    order = ForeignKey('apps.Order', CASCADE, related_name='order_items')
    product = ForeignKey('apps.Product', CASCADE, related_name='order_items')
    quantity = PositiveIntegerField(verbose_name=_('Quantity'), default=1)
    price = PositiveIntegerField(verbose_name=_('Price'))
