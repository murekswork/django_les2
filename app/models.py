from django.db import models
from accounts.models import Profile


class ProductCategories(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, default='Product')
    price = models.FloatField(default=99999)
    value = models.IntegerField(default=0)
    purchase_len = models.IntegerField(null=True, blank=True, default=0)
    rating = models.FloatField(default=5)
    description = models.CharField(max_length=1024, default='No description')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1024, default='https://image.shutterstock.com/image-vector/unknown-package-question-mark-260nw-1212499930.jpg')
    category = models.ForeignKey(ProductCategories, blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    def buy(self, value):
        self.value -= value
        self.purchase_len += 1
        self.save()


class PurchaseReview(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    rating = models.IntegerField(default=5)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Purchase(models.Model):
    buyer: Profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='buyer')
    saler: Profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='saler')
    product: Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)
    review = models.ForeignKey(PurchaseReview, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(default=999999)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, blank=True, null=True, default=None)
    is_payed = models.BooleanField(default=False, blank=False, null=False)

    def get_total_price(self):
        self.total_price = self.product.price * self.value
        return self.total_price


    def make_payment(self):
        if self.buyer.balance >= self.total_price and self.value <= self.product.value:
            self.buyer.balance -= self.total_price
            self.buyer.save()
            self.saler.balance += self.total_price
            self.saler.save()
            self.product.value -= self.value
            self.is_payed = True
            self.product.save()
            self.save()

class Cart(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    cart_discount = models.IntegerField(null=True, blank=True)
    cart_total_price = models.FloatField(default=0)

    def get_cart_total_price(self):
        summs = sum([purchase.total_price for purchase in self.purchase_set.select_related()])
        self.cart_total_price = summs
        return summs

    def proc_checkout(self):
        if self.profile.balance >= self.cart_total_price:
            for purchase in self.purchase_set.select_related():
                self.profile.save()
                purchase.make_payment()
                purchase.cart = None
                purchase.save()

            return {'success': True}
        else:
            return {'success': False, 'error': 'Not enough money!'}



# Create your models here.
