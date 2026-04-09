"""
Формы аутентификации и регистрации.
"""

from django import forms
from django.contrib.auth import authenticate, get_user_model

from .models import LearningMaterial


User = get_user_model()


class RegisterForm(forms.ModelForm):
    """
    Форма регистрации пользователя.
    """

    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Подтвердить пароль", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")

    def clean_username(self):
        """
        Проверяет уникальность логина.
        """
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким логином уже существует.")
        return username

    def clean(self):
        """
        Проверяет совпадение паролей.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")
        if password and password_repeat and password != password_repeat:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data

    def save(self, commit=True):
        """
        Создает пользователя с хэшированным паролем.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """
    Форма входа пользователя.
    """

    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        """
        Проверяет корректность логина и пароля.
        """
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Неверный логин или пароль.")
            cleaned_data["user"] = user
        return cleaned_data


class ProfileForm(forms.ModelForm):
    """
    Форма изменения личных данных пользователя.
    """

    class Meta:
        model = User
        fields = ("first_name", "last_name")


class CuratorMaterialForm(forms.ModelForm):
    """
    Форма создания учебного материала для куратора.
    """

    class Meta:
        model = LearningMaterial
        fields = (
            "title",
            "summary",
            "content",
            "attachment",
            "material_format",
            "category",
            "estimated_minutes",
            "is_published",
        )

    def clean_attachment(self):
        """
        Проверяет расширение прикрепленного файла.
        """
        attachment = self.cleaned_data.get("attachment")
        if not attachment:
            return attachment
        filename = attachment.name.lower()
        if not (filename.endswith(".pdf") or filename.endswith(".docx")):
            raise forms.ValidationError("Разрешены только файлы PDF или DOCX.")
        return attachment
