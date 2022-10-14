from unittest import TestCase

from authors.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Seu apelido'),
        ('email', 'Seu e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: da Silva'),
        ('password', 'Sua senha'),
        ('password2', 'Confirme sua senha'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('username', (
            'O nome de usuário deve conter letras, números ou um desses @.+-_.'
            'O comprimento deve estar entre 4 e 150 caracteres.'
        )),
        ('email', 'O e-mail deve ser válido.'),
        ('password', (
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O comprimento deve ter '
            'pelo menos 8 caracteres.'
        )),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @ parameterized.expand([
        ('username', 'Usuário'),
        ('first_name', 'Primeiro nome'),
        ('last_name', 'Último nome'),
        ('email', 'Endereço de email'),
        ('password', 'Senha'),
        ('password2', 'Confirmar senha'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': '1',
            'password2': '1',
        }
        return super().setUp(*args, **kwargs)

    @ parameterized.expand([
        ('username', 'Este campo não deve estar vazio'),
        ('first_name', 'Escreva seu primeiro nome'),
        ('last_name', 'Escreva seu sobrenome'),
        ('password', 'Senha não pode estar em branco'),
        ('password2', 'Por favor, repita sua senha'),
        ('email', 'O e-mail é obrigatório'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'O nome de usuário deve ter pelo menos 4 caracteres'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'O nome de usuário deve ter menos de 150 caracteres'

        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = (
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O comprimento deve ter '
            'pelo menos 8 caracteres.'
        )

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc1235'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Senha e senha2 devem ser iguais'

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'O e-mail do usuário já está em uso'
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))
