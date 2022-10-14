import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O comprimento deve ter '
            'pelo menos 8 caracteres.'
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu apelido')
        add_placeholder(self.fields['email'], 'Seu e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: da Silva')
        add_placeholder(self.fields['password'], 'Sua senha')
        add_placeholder(self.fields['password2'], 'Confirme sua senha')

    username = forms.CharField(
        label='Usuário',
        help_text=(
            'O nome de usuário deve conter letras, números ou um desses @.+-_.'
            'O comprimento deve estar entre 4 e 150 caracteres.'
        ),
        error_messages={
            'required': 'Este campo não deve estar vazio',
            'min_length': 'O nome de usuário deve ter pelo menos 4 caracteres',
            'max_length': 'O nome de usuário deve ter menos de 150 caracteres',
        },
        min_length=4, max_length=150,
    )
    first_name = forms.CharField(
        error_messages={'required': 'Escreva seu primeiro nome'},
        label='Primeiro nome'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Escreva seu sobrenome'},
        label='Último nome'
    )
    email = forms.EmailField(
        error_messages={'required': 'O e-mail é obrigatório'},
        label='Endereço de email',
        help_text='O e-mail deve ser válido.',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Senha',
        error_messages={
            'required': 'Senha não pode estar em branco'
        },
        help_text=(
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O comprimento deve ter '
            'pelo menos 8 caracteres.'
        ),
        validators=[strong_password]
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmar senha',
        error_messages={
            'required': 'Por favor, repita sua senha'
        },
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'O e-mail do usuário já está em uso', code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Senha e senha2 devem ser iguais',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
