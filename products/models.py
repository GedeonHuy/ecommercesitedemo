from django.db import models
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    title = models.CharField(_('Title'), max_length=120, blank=False)
    price = models.IntegerField(_('Price'))
    date_created = models.DateTimeField(auto_now_add=True)
    brand = models.CharField(_('Brand'), max_length=20, blank=False)
    description = models.CharField(_('Description'), max_length=3000, blank=True)
    image_url = models.CharField(_('Image URL'), max_length=3000, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title