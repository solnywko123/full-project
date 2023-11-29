from django.db import models
from django.contrib.auth import get_user_model
from apps.category.models import Category

User = get_user_model()


# Create your models here.
class Product(models.Model):
    STATUS_CHOISES = (
        ('in_stock', "В наличии"),
        ('out_of_stock', "Нет в наличии")
    )

    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='products')
    title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.RESTRICT)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.CharField(choices=STATUS_CHOISES, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title





