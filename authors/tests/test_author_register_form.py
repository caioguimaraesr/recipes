from unittest import TestCase # Utilizado para o Teste Unitário
from django.test import TestCase as DjangoTestCase # Utilizado para o Teste Integrado
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex: Caio'),
        ('last_name', 'Ex: Rocha'),
        ('username', 'Choose your username'),
        ('email', 'Put you email'),
        ('password', 'Create your password'),
        ('confirm_password', 'Confirm your password'),
    ])
    def test_fields_placeholder(self, field, text):
        form = RegisterForm()
        current = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current, text)

    @parameterized.expand([
        ('password', 'Passoword must have at least one uppercase letter, one lowercase letter and one number. The lenght should be at leat 8 characters'),
    ])
    def test_help_text_is_correct(self,field,text):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, text)
    
    @parameterized.expand([
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('username', 'Username'),
        ('email', 'Email'),
        ('password', 'Password'),
        ('confirm_password', 'Confirm Password'),
    ])
    def test_fields_label(self, field, text):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, text)

class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username':'user',
            'first_name': 'first',
            'last_name':'last',
            'email':'email@email.com',
            'password':'Strongpassword1',
            'confirm_password':'Strongpassword1'
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('first_name', 'The field most be empty'),
        ('last_name', 'The field most be empty'),
        ('username', 'The field most be empty'),
        ('email', 'The field most be empty'),
        ('password', 'The field most be empty'),
        ('confirm_password', 'The field most be empty'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].erros.get(field))

    def test_username_field_min_lenght_should_be_44(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)