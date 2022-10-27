from django.db import models
from accounts.models import Profile


class Product(models.Model):
    name = models.CharField(max_length=100, default='Product')
    price = models.FloatField(default=99999)
    value = models.IntegerField(default=0)
    rating = models.FloatField(default=5)
    description = models.CharField(max_length=1024, default='No description')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1024, default='https://image.shutterstock.com/image-vector/unknown-package-question-mark-260nw-1212499930.jpg')


class PurchaseReview(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    rating = models.IntegerField(default=5)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Purchase(models.Model):
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='buyer')
    saler = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='saler')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)
    review = models.ForeignKey(PurchaseReview, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(default=999999)

    def get_total_price(self):
        self.total_price = self.product.price * self.value
        return self.total_price



# Create your models here.
