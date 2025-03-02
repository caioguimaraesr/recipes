from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import strong_password

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
        help_text='Username must have letters, numbers or one of those @.+=_/. The length should be between 4 and 150 characters',
        min_length=4, max_length=150,
        error_messages={
            'required':'The field most be empty',
            'unique':'User already exists',
            'min_length':'Username must have at least 4 characters.',
            'max_length':'Username must have less than 150 characters'
        },
    )

    email = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder':'Put you email'
        }),
        label='Email',
        error_messages={
            'required':'The field most be empty',
            'invalid':'Invalid Email. Fill in the field correctly',
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
            'placeholder': 'Confirm your password'
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
            'username',
            'email',
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
        
    # Email já existente.
    def clean_email(self):
        email = self.cleaned_data.get('email')

        error = ValidationError(
            'Email already exists'
        )

        if User.objects.filter(email=email).exists():
            raise error
        return email