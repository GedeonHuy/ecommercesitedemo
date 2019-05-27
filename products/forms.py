from .models import Product
from django.forms import ModelForm 

from django.contrib.auth import forms

class ProductForm(ModelForm):
    class Meta(ModelForm):
        model = Product
        fields = (
            'title',
            'price',
            'description',
            'brand',
            'image_url',
        )