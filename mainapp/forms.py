from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginUserForm(AuthenticationForm):

    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-signin',
                'placeholder': 'Имя пользователя',
                'id': 'username',
            }
        )
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control input-signin',
                'placeholder': 'Введите пароль'
            }
        )
    )
