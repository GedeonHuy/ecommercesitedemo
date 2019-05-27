from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import ProductForm
from .models import Product


class Index(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'products'
    ordering = ['-date_created']

class Create(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product_index')
    template_name = 'products/create.html'

class Update(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product_index')
    template_name = 'products/update.html'

class Detail(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'

class Delete(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product_index')
    template_name = 'products/delete.html'
    context_object_name = 'product'
