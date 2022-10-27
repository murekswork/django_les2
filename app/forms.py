from django import forms
from django.forms import ModelForm
from .models import Product

class ProductForm(ModelForm):


    class Meta:
        model = Product
        exclude = ['rating', 'profile']