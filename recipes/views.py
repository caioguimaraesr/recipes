from django.db.models import Q # Usado para dizer para o django que eu nao quero usar o AND e sim o OR 
from django.shortcuts import render
from recipes.models import Recipe
from django.http import Http404
from django.core.paginator import Paginator
from utils.pagination import make_pagination
import os

PER_PAGE = int(os.environ.get('PER_PAGE', 3))

# Create your views here.
def home(request):
    recipes = (
        Recipe.objects.filter(
            is_published=True,
        ).order_by('-id')
    ) # queryset

    page_obj, pagination_range = make_pagination(request,recipes,PER_PAGE)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range
    })

def category(request, category_id):
    recipes =(
        Recipe.objects.filter(
            category__id=category_id, 
            is_published=True,
        ).order_by('-id')
    ) # queryset

    page_obj, pagination_range = make_pagination(request,recipes,PER_PAGE)
    
    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title':f'{recipes.first().category.name}'
    })

def recipes(request, id):
    recipe = Recipe.objects.get(pk=id, is_published=True) # queryset

    if not recipes:
        return render(request, 'recipes/pages/notFound.html', status=404)
    
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })

def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    
    # "<elementos_dos_models>__icontains" vai aceitar maiuscula, minuscula...
    recipes = Recipe.objects.filter(
        Q(title__icontains = search_term) | 
        Q(description__icontains = search_term),
        is_published = True
    ).order_by('-id') # queryset

    page_obj, pagination_range = make_pagination(request,recipes,PER_PAGE)
    
    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for "{search_term}" | Recipes',
        'search_term': search_term,
        'recipes': page_obj, # Paginator
        'pagination_range': pagination_range, # Paginator
        'additional_url_query':f'&q={search_term}', # Paginator
    })