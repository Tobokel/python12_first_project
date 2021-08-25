from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    class Meta:
        ordering = ['title', 'price']
    def __str__(self):
        return self.title

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    text = models.TextField()
    rating = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

