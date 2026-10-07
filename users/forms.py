from django.contrib.auth.forms import UserCreationForm, forms
from django.core.exceptions import ValidationError

from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"class": "form-control"})

        self.fields["password1"].widget.attrs.update({"class": "form-control"})

        self.fields["password2"].widget.attrs.update({"class": "form-control"})

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с такой электронной почтой уже существует")

        return email


class ChangeProfileUser(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = (
            "password",
            "is_active",
            "is_staff",
            "date_joined",
            "groups",
            "is_superuser",
            "user_permissions",
            "last_login",
        )

    def __init__(self, *args, **kwargs):
        super(ChangeProfileUser, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Введите Ник"})

        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Ваше имя"})

        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Ваша фамилия"})

        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Электронная почта"})

        self.fields["phone_number"].widget.attrs.update({"class": "form-control", "placeholder": "Телефон"})

    def clean(self):
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")

        if first_name and last_name:
            if CustomUser.objects.filter(first_name=first_name, last_name=last_name).exists():
                raise ValidationError("Пользователь с таким Именем и Фамилией уже существует")

        return self.cleaned_data


class RecoveryPasswordForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(RecoveryPasswordForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Ваша электронная почта"})

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not CustomUser.objects.filter(email=email):
            raise ValidationError("Пользователь с такой почтой не найден \nПопробуйте ввести другую")

        return email
