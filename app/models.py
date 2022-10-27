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

# Create your models here.
