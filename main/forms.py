from django import forms
from django.contrib.auth.models import User
from .models import GameRequest, UserGame


# ---------------------------
# Форма регистрации пользователя
# ---------------------------
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")

        return cleaned_data


# ---------------------------
# Форма для добавления игры пользователем
# ---------------------------
class UserGameForm(forms.ModelForm):
    class Meta:
        model = UserGame
        fields = ['title', 'description', 'size', 'seeds', 'image', 'screenshot', 'trailer_url', 'download_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['size'].required = False
        self.fields['seeds'].required = False

    def clean_size(self):
        return self.cleaned_data.get('size') or 0

    def clean_seeds(self):
        return self.cleaned_data.get('seeds') or 0


# ---------------------------
# Форма для запроса новой игры (GameRequest)
# ---------------------------
class GameRequestForm(forms.ModelForm):
    class Meta:
        model = GameRequest
        fields = ['name', 'description', 'requirements', 'reviews', 'trailer_url', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'reviews': forms.Textarea(attrs={'rows': 4}),
        }
