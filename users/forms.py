from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "password1", "password2")
