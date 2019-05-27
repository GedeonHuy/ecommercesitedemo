from django.views.generic.base import TemplateView
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Profile.as_view(), name='view_profile'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('update/<int:pk>/', views.Update.as_view(), name='update_profile'),
    path('update/password/', views.PasswordChange.as_view(), name='change_password'),
]