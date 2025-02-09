from django.core.exceptions import ValidationError
import re

# Senha forte
def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$') # Expressão regular

    if not regex.match(password):
        raise ValidationError('Enter a strong password to protect your account', code='invalid')