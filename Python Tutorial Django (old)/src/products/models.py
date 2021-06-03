from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)  # max_length required
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10000)
    summary = models.TextField(blank=False, null=False)  # if blank is False --> input is required
    features = models.BooleanField()  # null=True, default=True

'''
create new products:

python manage.py shell
from products.models import Product
Product.objects.all()
Product.objects.create(title="2", description="new", price="123", summary="goof!")
'''