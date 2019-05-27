import datetime
import random
import string
from datetime import date

import stripe
from django import template
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView

from products.models import Product
from users.models import CustomUser, Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

class HomePageView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    ordering = ['-date_created']

class OrderDetail(LoginRequiredMixin, ListView):
    model = OrderItem
    template_name = 'payment/order_detail.html'
    context_object_name = 'order_items'
    ordering = ['-date_created']

    def get_order_items(self, *args):
        try:
            # get current logged in user
            current_order = get_object_or_404(Order, ref_code=args[0])
        except: 
            current_order = ''
        if (current_order != ''):
            object_list = current_order.items.all()
        else:
            object_list = self.model.objects.all()

        return object_list

    def get(self, request, **kwargs):
        self.object_list = self.get_order_items(kwargs.get('ref_code', ""))
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        
        context = self.get_context_data()
        return self.render_to_response(context)

class OrderDone(LoginRequiredMixin, TemplateView):
    template_name = 'payment/order_done.html'

class OrderHistory(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'payment/order_history.html'
    context_object_name = 'orders'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """Get the context for this view."""
        queryset = object_list if object_list is not None else self.object_list
        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset,
                
                # payment api needs these
                'key': settings.STRIPE_PUBLISHABLE_KEY,
                'price': 0
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset,
                
                # payment api needs these
                'key': settings.STRIPE_PUBLISHABLE_KEY,
                'price': 0
            }
        if context_object_name is not None:
            context[context_object_name] = queryset
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_orders(self, *args):
        try:
            # get current logged in user
            current_user = get_object_or_404(CustomUser, username=args[0])
        except: 
            current_user = ''
        if (current_user != ''):
            object_list = self.model.objects.filter(owner=current_user)
        else:
            object_list = self.model.objects.all()

        return object_list

    def get(self, request):
        self.object_list = self.get_orders(request.user.username)
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        
        context = self.get_context_data()
        return self.render_to_response(context)

@login_required()
def order_cart(request):
    # get current logged in user
    current_user = get_object_or_404(CustomUser, username=request.user.username)
    # get his pending order
    pending_orders = Order.objects.filter(owner=current_user, is_ordered=False)
    # make sure 'context' is cleared from last checkout
    context = {
        'order_items': None,
        'key': None,
        'price': None,
    }
    if pending_orders.exists():
        context = {
            'order_items': pending_orders[0],
            'key': settings.STRIPE_PUBLISHABLE_KEY,
            'price': 0,
        }
    
    template_name = 'payment/cart.html'
    return render(request, template_name, context)

def charge(request, **kwargs):
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=kwargs.get('price',""),
            currency='usd',
            description='Checkout successful.',
            source=request.POST['stripeToken']
        )

        # get current logged in user
        current_user = get_object_or_404(CustomUser, username=request.user.username)
        # update his pending order's ordered status to is_ordered=True
        # update his pending order items' checkedout status to is_checkedout=True
        Order.objects.filter(owner=current_user, is_ordered=False).update(is_ordered=True, date_checkedout=datetime.datetime.now(), is_checkedout=True)

        return redirect(reverse_lazy('order_done'))
    return redirect(reverse_lazy('cart'))

@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    current_user = CustomUser.objects.filter(id=request.user.id).first()

    # filter products by id
    product = Product.objects.filter(id=kwargs.get('product_id', "")).first()

    # create orderItem of the selected product
    order_item, item_status = OrderItem.objects.get_or_create(product=product)

    # create order associated with the user
    user_order, order_status = Order.objects.get_or_create(owner=current_user, is_ordered=False)
    user_order.items.add(order_item)
    # add this order item price to this order total price
    if item_status:
        user_order.total_price += order_item.product.price

    if order_status:
        # generate a reference code and total_price
        user_order.ref_code = generate_order_id()
        user_order.save()

    user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('product_detail', args=kwargs.get('product_id', "")))

@login_required()
def delete_from_cart(request, item_id):
    order_item_to_delete = OrderItem.objects.filter(pk=item_id)

    # get the current user profile and order 
    current_user = CustomUser.objects.filter(id=request.user.id).first()
    user_order = Order.objects.get_or_create(owner=current_user, is_ordered=False)
    # have this delete item's price from total price substraction

    if order_item_to_delete.exists():
        item_price = order_item_to_delete[0].product.price
        order_item_to_delete[0].delete()
        user_order[0].total_price -= item_price
        user_order[0].save()
        messages.info(request, "Item has been deleted")
    
    return redirect(reverse_lazy('cart'))

def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str
