from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from .apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("register_user/", views.RegistrationUserCreateView.as_view(), name="register_user"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile_user/<int:pk>/", views.ProfileUser.as_view(), name="profile_user"),
    path("change_profile/<int:pk>/", views.ProfileUserUpdateView.as_view(), name="change_profile"),
]
