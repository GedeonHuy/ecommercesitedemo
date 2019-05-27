from . import views
from users import urls as custom_user_urls
from django.urls import path, include
from django.contrib.auth import urls as default_user_urls
from django.views.generic.base import TemplateView
from django.contrib.auth import views as default_views
from users import views as signup_views

urlpatterns = [
    path('', views.Index.as_view(), name='product_index'),
    path('create/', views.Create.as_view(), name='product_create'),
    path('create/user/login/', default_views.LoginView.as_view(), name='productcreate_login'),
    path('<int:pk>/', views.Detail.as_view(), name='product_detail'),
    path('<int:pk>/update/', views.Update.as_view(), name='product_update'),
    path('<int:pk>/update/user/login/', default_views.LoginView.as_view(), name='productupdate_login'),
    path('<int:pk>/delete/', views.Delete.as_view(), name='product_delete'),
    path('<int:pk>/delete/user/login/', default_views.LoginView.as_view(), name='productdelete_login'),
    path('user/login/', default_views.LoginView.as_view(), name='product_login'),
    path('user/signup/', signup_views.SignUp.as_view(), name='product_signup'),
]