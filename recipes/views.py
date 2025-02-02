from django.shortcuts import render, get_list_or_404
from utils.recipes.factory import make_recipe
from recipes.models import Recipe
from django.http import Http404, HttpResponse

# Create your views here.
def home(request):
    recipes = (
        Recipe.objects.filter(
            is_published=True,
        ).order_by('-id')
    )
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })

def category(request, category_id):
    recipes =(
        Recipe.objects.filter(
            category__id=category_id, 
            is_published=True,
        ).order_by('-id')
    )
    
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title':f'{recipes.first().category.name}'
    })

def recipes(request, id):
    recipe = Recipe.objects.get(pk=id, is_published=True)

    if not recipes:
        return render(request, 'recipes/pages/notFound.html', status=404)
    
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })
