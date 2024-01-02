from django.db import models
from django.contrib.auth.models import User


class CustomManager(models.Manager):
    def get_price_range(self, r1, r2):
        return self.filter(price__range=(r1, r2))

    def mobile_list(self):
        return self.filter(category__exact="Mobile")

    def cloths_list(self):
        return self.filter(category__exact="Cloths")

    def shoes_list(self):
        return self.filter(category__exact="Shoes")


# Create your models here.
class Product(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=55)
    type = (("Mobile", "Mobile"), ("Cloths", "Cloths"), ("Shoes", "Shoes"))
    category = models.CharField(max_length=100, choices=type, default="")
    desc = models.TextField(max_length=255)
    price = models.IntegerField()
    image = models.ImageField(upload_to="pics")
    objects = models.Manager()
    prod = CustomManager()


class Cart(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    userid = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)