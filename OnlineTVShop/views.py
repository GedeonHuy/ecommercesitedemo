from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from products.models import Product


class Home(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    ordering = ['-date_created']

class Others(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    ordering = ['-date_created']

    def get_queryset(self):
        try:
            name = 'Others'
        except:
            name = ''
        if (name != ''):
            object_list = self.model.objects.filter(~Q(brand='Sony'), ~Q(brand='Samsung'), ~Q(brand='LG'), ~Q(brand='Sharp'))
        else:
            object_list = self.model.objects.all()
        return object_list

class SearchTV(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    ordering = ['title', 'brand', 'description', '-date_created']

    def get_searchedtv(self, *arg):
        try:
            search_string = arg[0]
        except: 
            search_string = ''
        if (search_string != ''):
            object_list = self.model.objects.filter((Q(brand__icontains=search_string) | Q(title__icontains=search_string)) | Q(description__icontains=search_string))
        else:
            object_list = self.model.objects.all()

        return object_list

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_searchedtv(kwargs.get('string', ""))
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

class SearchBrand(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    ordering = ['title', 'brand', 'description', '-date_created']

    def get_searchedtv(self, *arg):
        try:
            search_string = arg[0]
        except: 
            search_string = ''
        if (search_string != ''):
            object_list = {}
            if (search_string == 'sony') or (search_string == 'samsung') or (search_string == 'sharp') or (search_string == 'lg'):
                object_list = self.model.objects.filter(brand__icontains=search_string)
        else:
            object_list = self.model.objects.all()

        return object_list

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_searchedtv(kwargs.get('string', ""))
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

def search(request):
    request_kwargs = {
        'string':request.GET.get('search', "")
    }
    return redirect(reverse('search_tv', kwargs=request_kwargs))
