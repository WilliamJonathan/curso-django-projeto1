from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        # exclude = ['first_name]
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobre nome',
            'username': 'Apelido',
            'email': 'E-mail',
            'password': 'Senha',
        }
        help_texts = {
            'email': 'Precisa ser um email valido'
        }
        error_messages = {
            'username': {
                'required': 'Campo não pode estar em branco',
            }
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Informe seu primeiro nome aqui'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Escolha uma senha'
            })
        }
