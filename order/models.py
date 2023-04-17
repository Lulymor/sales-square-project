from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    status = models.CharField(
        default='C',
        max_length=1,
        choices=(
            ('A', 'Approved'),
            ('C', 'Created'),
            ('D', 'Denied'),
            ('P', 'Pending'),
            ('S', 'Shipping'),
            ('D', 'Delivered'),
        )
    )

    def __str__(self):
        return f'Order N. {self.pk}'


class ItemOrdered(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=255)
    product_id = models.PositiveIntegerField()
    variation = models.CharField(max_length=50)
    variation_id = models.PositiveIntegerField()
    price = models.FloatField()
    sale_price = models.FloatField(default=0)
    amount = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item of the {self.order}'

    class Meta:
        verbose_name = 'Item of the order'
        verbose_name_plural = 'Items of the order'
