from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import ChangeProfileUser, UserRegistrationForm
from .models import CustomUser


class RegistrationUserCreateView(CreateView):
    """
    Представление для регистрации пользователя
    """

    model = CustomUser
    form_class = UserRegistrationForm
    template_name = "users/register_user.html"
    success_url = reverse_lazy("users:login")


class ProfileUser(DetailView):
    """
    Представление для детальной информации о пользователе
    """

    model = CustomUser
    template_name = "users/profile_user.html"
    context_object_name = "user"


class ProfileUserUpdateView(UpdateView):
    """
    Представление для изменения профиля пользователя
    """

    model = CustomUser
    form_class = ChangeProfileUser
    template_name = "users/change_profile.html"
    context_object_name = "user"

    def get_success_url(self):
        return reverse_lazy("users:profile_user", kwargs={"pk": self.object.pk})
