from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views

class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id':1}))
        self.assertIs(view.func, views.category)
    
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipes)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_returns_templates(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)
    
    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    