"""OnlineTVShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.contrib import admin
from django.contrib.auth import urls as default_user_urls
from django.urls import include, path
from django.views.generic.base import TemplateView

from payments import urls as payment_urls
from products import urls as product_urls
from users import urls as custom_user_urls

from . import views

urlpatterns = [
    # home/about/contact page
    path('', views.Home.as_view(), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),

    # filter/search engine for brand specifically or digging into product's brand, search and description
    path('brand/<string>/', views.SearchBrand.as_view(), name='search_brand'),
    path('search/<string>/', views.SearchTV.as_view(), name='search_tv'),
    path('others/', views.Others.as_view(), name='others_filter'),
    path('search/', views.search, name='search'),
    
    # user/customer account management urls
    path('admin/', admin.site.urls),
    path('user/', include(custom_user_urls)),
    path('user/', include(default_user_urls)),

    # product management urls
    path('product/', include(product_urls)),

    # payment management urls
    path('shopping/', include(payment_urls)),
]
