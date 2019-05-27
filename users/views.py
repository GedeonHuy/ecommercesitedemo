from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class Update(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('view_profile')
    template_name = 'registration/update.html'

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    model = CustomUser
    success_url = reverse_lazy('password_change_done')

class Profile(TemplateView):
    template_name = 'registration/profile.html'

""" def my_profile(request):
	my_user_bill = Profile.objects.filter(user=request.user).first()
	my_orders = Order.objects.filter(is_ordered=True, owner=my_user_bill)
	context = {
		'my_orders': my_orders
	}

	return render(request, "registration/bill.html", context) """

""" def view_profile(request):
    current_user = request.user
    template_name = 'registration/profile.html'
    context = {
        'form': None,
        'user_id': current_user.id
    }
    return render(request, template_name, context) """
