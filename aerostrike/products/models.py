from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Product(models.Model):
    PRODUCT_TYPE = (
        ('jet', 'Fighter Jet'),
        ('missile', 'Missile'),
    )

    name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE)
    description = models.TextField()
    price = models.BigIntegerField()
    range_km = models.IntegerField()
    speed = models.CharField(max_length=100)

    image = models.ImageField(upload_to='products/')
    distributor = models.ForeignKey(User, on_delete=models.CASCADE)

    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Create your models here.
