from django import forms
from recipes.models import Recipe
from collections import defaultdict # validação dos erross
from django.core.exceptions import ValidationError

class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list) 

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'category',
            'preparation_step',
            'cover',
        ]

        widgets= {
            'preparation_step': forms.Textarea(attrs={
                'class':'span-2'
            }),
            'cover': forms.FileInput(attrs={
                'class':'span-2'
            }),
            'category': forms.Select(attrs={
                'class':'span-2'
            }),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Perdaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                ),
            ),
        }

    # Forma mais fácil de fazer uma validação com o defaultdict
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')

        # Erro 1
        if title == description:
            self._my_errors['title'].append('The title cannot be the same as the description.')
            self._my_errors['description'].append('The title cannot be the same as the description.')

        # Levanta o erro 
        if self._my_errors:
            raise ValidationError(self._my_errors)
        
        return super_clean
    
    # Erro 2
    def clean_title(self):
        field_name = 'title'

        field_value = self.cleaned_data.get(field_name)

        if len('title') > 5:
            self._my_errors[field_name].append('Must have at least 5 characters')

        return field_value
    
    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')

        try:
            preparation_time = float(preparation_time)  
            if preparation_time <= 0:
                raise ValueError
        except (TypeError, ValueError):  
            raise ValidationError('Must be a positive number.')

        return preparation_time
    
    def clean_servings(self):
        servings = self.cleaned_data.get('servings')

        try:
            servings = float(servings)  
            if servings <= 0:
                raise ValueError
        except (TypeError, ValueError):  
            raise ValidationError('Must be a positive number.')

        return servings