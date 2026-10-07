from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import UserRegistrationForm
from .models import CustomUser


class RegistrationUserCreateView(CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = "users/register_user.html"
    success_url = reverse_lazy("users:login")


class ProfileUser(DetailView):
    model = CustomUser
    template_name = "users/profile_user.html"
    context_object_name = "user"
