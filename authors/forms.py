from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

# Senha forte
def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$') # Expressão regular

    if not regex.match(password):
        raise ValidationError(('Enter a strong password to protect your account'), code='invalid')

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: Caio'
        }),
        label = "First Name",
        error_messages={
            'required':'The field most be empty'
        }
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: Rocha'
        }),
        label="Last Name",
        error_messages={
            'required':'The field most be empty'
        }
    )

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Choose your username'
        }),
        label="Username",
        error_messages={
            'required':'The field most be empty'
        }
    )

    email = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder':'Put you email'
        }),
        label='Email',
        error_messages={
            'required':'The field most be empty',
            'invalid':'Invalid Email. Fill in the field correctly'
        }
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create your password'
        }),
        label='Password',
        help_text='Passoword must have at least one uppercase letter, one lowercase letter and one number. The lenght should be at leat 8 characters',
        error_messages={
            'required':'The field most be empty'
        },
        validators=[strong_password]
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm you password'
        }),
        label='Confirm Password',
        error_messages={
            'required':'The field most be empty'
        }
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
        ]


    # Senhas iguais
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            error = ValidationError(
                'The password must be equal', code = 'invalid'
            )
        
            raise ValidationError({
                'password': error,
                'confirm_password': error
            })