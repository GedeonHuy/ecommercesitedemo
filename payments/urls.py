from django.contrib.auth import urls as default_user_urls
from django.urls import path, include
from . import views
from django.contrib.auth import views as default_views
from users import views as signup_views

urlpatterns = [
    path('order/history/', views.OrderHistory.as_view(), name='history'),
    path('order/<ref_code>/', views.OrderDetail.as_view(), name='order_detail'),
    path('order/done/', views.OrderDone.as_view(), name='order_done'),
    path('order/done/user/login/', default_views.LoginView.as_view(), name='orderdone_login'),
    path('cart/', views.order_cart, name='cart'),
    path('cart/user/login/', default_views.LoginView.as_view(), name='cart_login'),
    path('charge/<price>/', views.charge, name='charge'),
    path('charge/<price>/user/login/', default_views.LoginView.as_view(), name='charge_login'),
    path('add_to_cart/<product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_cart/<product_id>/user/login/', default_views.LoginView.as_view(), name='tocart_login'),
    path('delete_from_cart/<item_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('delete_from_cart/<item_id>/user/login/', default_views.LoginView.as_view(), name='deletefrom_login'),
    path('user/signup/', signup_views.SignUp.as_view(), name='payment_signup'),
]
