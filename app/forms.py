from django import forms
from django.forms import ModelForm
from .models import Product, Purchase, PurchaseReview

class ProductForm(ModelForm):


    class Meta:
        model = Product
        exclude = ['rating', 'profile']



class PurchaseForm(ModelForm):

    value = forms.IntegerField()
    class Meta:
        model = Purchase
        exclude = ['buyer', 'review', 'saler', 'product', 'review_id', 'date', 'total_price']

RATING_CHOICES = [('ONE', 1), ('TWO', 2), ('THREE', 3), ('FOUR', 4), ('FIVE', 5)]
class ReviewForm(ModelForm):

    rating = forms.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = PurchaseReview
        fields = ['title', 'description', 'rating']
        exclude = ['product']