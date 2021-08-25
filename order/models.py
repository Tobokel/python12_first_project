from django.contrib.auth import get_user_model
from django.db import models

from product.models import Product

User = get_user_model()
STATUS_CHOICES = (
    ('open', 'Открытый'),
    ('in_progress', 'В обработке'),
    ('cancelled', 'Отмененный'),
    ('finished', 'Завершенный')
)


class Order(models.Model):
    total_sum = models.DecimalField(max_digits=10,
                                    decimal_places=2,
                                    default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User,
                             on_delete=models.RESTRICT,
                             related_name='orders')

    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='open')

    products = models.ManyToManyField(Product,
                                     through='OrderItem')
    @property
    def total(self):
        items = self.items.values('product__price', 'quantity')
        total = 0
        for item in items:
            total += item['product__price'] * item['quantity']
        return total

    def __str__(self):
        return f'Заказ № {self.id} от {self.created_at.strftime("%d-%m-%Y %H:%M")}'

    class Meta:
        db_table = 'order'
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.RESTRICT,
                              related_name='items')

    product = models.ForeignKey(Product,
                                on_delete=models.RESTRICT,
                                related_name='order_item')

    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table = 'order_items'

