from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product
""" from django.db.models.signals import post_save
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY """

class CustomUser(AbstractUser):
    # add additional fields in here
    dob = models.DateField(_('Date of birth'), max_length=8, blank=True, null=True)
    address = models.CharField(_('Address'), max_length=120, blank=True, null=True)
    
    def __str__(self):
        return self.username

class OrderItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)
    is_checkedout = models.BooleanField(default=False)
    date_checkedout = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title

class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)
    date_checkedout = models.DateTimeField(null=True)
    is_checkedout = models.BooleanField(default=False)
    total_price = models.IntegerField(_('Total Price'), default=0)

    def get_count(self):
        return len(self.get_cart_items())

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)

""" def post_save_bill_create(sender, instance, created, *args, **kwargs):
    user_bill, created = CustomerBill.objects.get_or_create(user=instance)

    if user_bill.stripe_id is None or user_bill.stripe_id == '':
        new_stripe_id = stripe.Customer.create(email=instance.email)
        user_bill.stripe_id = new_stripe_id['id']
        user_bill.save()


post_save.connect(post_save_bill_create, sender=settings.AUTH_USER_MODEL) """