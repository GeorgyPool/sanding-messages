import secrets

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  UpdateView)

from config.settings import EMAIL_HOST_USER

from .forms import (ChangeProfileUser, RecoveryPasswordForm,
                    UserRegistrationForm)
from .models import CustomUser


class RegistrationUserCreateView(CreateView):
    """
    Представление для регистрации пользователя
    """

    model = CustomUser
    form_class = UserRegistrationForm
    template_name = "users/register_user.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/checking/{token}/"
        send_mail(subject="Подтверждение почты", message=url, from_email=EMAIL_HOST_USER, recipient_list=[user.email])

        return super().form_valid(form)


class CustomLogView(LoginView):
    """
    Представление для входа на сайт
    """

    template_name = "users/login.html"
    success_url = reverse_lazy("sending:home")

    def form_invalid(self, form):
        """
        Проверяет чтобы пользователь подтвердил почту
        """
        email = form.cleaned_data.get("username")

        try:
            user = CustomUser.objects.get(email=email)
            if not user.is_active:
                form.add_error(None, "Подтвердите почту")
        except CustomUser.DoesNotExist:
            form.add_error(None, "Почта не найдена")

        return super().form_invalid(form)


def verification_user(request, token):
    user = CustomUser.objects.get(token=token)
    user.is_active = True
    user.save()
    return render(request, "users/checking.html")


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


class PasswordRecoveryFormView(FormView):
    """
    Представление для восстановления пароля
    """

    template_name = "users/password_recovery.html"
    form_class = RecoveryPasswordForm
    success_url = reverse_lazy("sending:home")

    def form_valid(self, form):
        response = form.cleaned_data.get("email")
        user = CustomUser.objects.get(email=response)
        host = self.request.get_host()

        send_mail(
            subject="Восстановление пароля",
            message=f"http://{host}/users/change_password/{user.token}/",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user],
        )
        return super().form_valid(form)


def change_password(request, token):
    user = CustomUser.objects.get(token=token)
    if request.method == "POST":
        password = request.POST.get("password")
        user.set_password(password)
        user.save()
        return redirect(reverse("users:login"))

    context = {"user": user}
    return render(request, "users/change_password.html", context=context)


class AllUsersListView(PermissionRequiredMixin, ListView):
    """
    Представление для менеджеров: отображает список всех пользователей.
    PermissionRequiredMixin автоматически проверяет права без них будет 403.
    """

    model = CustomUser
    template_name = "users/all_users.html"
    context_object_name = "users"
    permission_required = "users.management"


class ChangedUserPermission(PermissionRequiredMixin, UpdateView):
    model = CustomUser
    fields = ["is_active"]
    template_name = "users/change_profile_user_manager.html"
    success_url = reverse_lazy("users:all_users")
    permission_required = "users.management"
