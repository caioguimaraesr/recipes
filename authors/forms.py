from django import forms
from django.contrib.auth.models import User

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
        help_text='É necessário uma letra maíuscula, uma minuscula e um número.',
        error_messages={
            'required':'The field most be empty'
        }
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