"""
Формы аутентификации и регистрации.
"""

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.forms import inlineformset_factory

from .models import LearningMaterial, MaterialPage


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


class MaterialPageForm(forms.ModelForm):
    """
    Одна страница материала: текст, изображение, опциональный мини-тест.
    """

    class Meta:
        model = MaterialPage
        fields = (
            "title",
            "body",
            "image",
            "quiz_question",
            "quiz_choice_1",
            "quiz_choice_2",
            "quiz_choice_3",
            "quiz_choice_4",
            "quiz_correct",
        )
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Необязательно"}),
            "body": forms.Textarea(attrs={"rows": 8, "class": "material-page-body"}),
            "quiz_question": forms.Textarea(attrs={"rows": 2}),
            "quiz_choice_1": forms.Textarea(attrs={"rows": 1}),
            "quiz_choice_2": forms.Textarea(attrs={"rows": 1}),
            "quiz_choice_3": forms.Textarea(attrs={"rows": 1}),
            "quiz_choice_4": forms.Textarea(attrs={"rows": 1}),
            "quiz_correct": forms.Select(
                choices=[("", "—")] + [(i, str(i)) for i in range(1, 5)]
            ),
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            return image
        name = getattr(image, "name", "") or ""
        lower = name.lower()
        if not lower.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")):
            raise forms.ValidationError("Допустимы изображения: JPG, PNG, GIF, WEBP.")
        return image


MaterialPageFormSet = inlineformset_factory(
    LearningMaterial,
    MaterialPage,
    form=MaterialPageForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
