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
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_lenght_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have at least 4 characters.)'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_lenght_should_be_150(self):
        self.form_data['username'] = 'a' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have less than 150 characters'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Enter a strong password to protect your account'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
    
    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Enter a strong password to protect your account'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        

        self.form_data['password'] = '@A123abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.context['form'].errors.get('password'))
    
    def test_password_and_confirm_password_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['confirm_password'] = '@A123abc1234'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'The password must be equal'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        

        self.form_data['password'] = '@A123abc123'
        self.form_data['confirm_password'] = '@A123abc123'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_gest_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_most_be_unique(self):
        url = reverse('authors:create')

        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Email already exists'
        
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))