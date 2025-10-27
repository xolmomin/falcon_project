from django.db.models import CharField, PositiveIntegerField, \
    ForeignKey, CASCADE, TextChoices, DateField
from django.db.models.fields import PositiveSmallIntegerField
from django.utils.translation import gettext_lazy as _

from apps.models.base import CreatedBaseModel


class Order(CreatedBaseModel):
    class Status(TextChoices):
        IN_PROGRESS = 'in_progress', 'In progress'
        PAID = 'paid', 'Paid'
        CANCELED = 'canceled', 'Canceled'

    class PaymentType(TextChoices):
        CASH = 'cash', 'Cash'
        ONLINE = 'online', 'Online'

    card_number = CharField(verbose_name=_('Card Number'), max_length=20, null=True, blank=True)
    exp_date = CharField(verbose_name=_('Exp Date'), max_length=4, null=True, blank=True)
    cvv = PositiveSmallIntegerField(verbose_name=_('CVV'), null=True, blank=True)

    payment_type = CharField(choices=PaymentType.choices, default=PaymentType.ONLINE)
    user = ForeignKey('apps.User', CASCADE, related_name='orders')
    status = CharField(max_length=255, default=Status.IN_PROGRESS, choices=Status.choices)
    total_price = PositiveIntegerField(verbose_name=_('Total Price'), null=True, blank=True)


class OrderItem(CreatedBaseModel):
    order = ForeignKey('apps.Order', CASCADE, related_name='order_items')
    product = ForeignKey('apps.Product', CASCADE, related_name='order_items')
    quantity = PositiveIntegerField(verbose_name=_('Quantity'), default=1)
    price = PositiveIntegerField(verbose_name=_('Price'))
