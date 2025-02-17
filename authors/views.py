from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe
from authors.forms.recipe_form import AuthorRecipeForm
from django.utils.text import slugify

def register_view(request): # GET
    register_form_data = request.session.get('register_form_data', None) # 4- Vai armazenas os dados na variável 'register_form_data', caso não tenha nada, será None
    form = RegisterForm(register_form_data) # 5- Caso for for None (Deu tudo certo com a outra sessão) inciará sem nada, se contiver dados na sessão será exibido os erros para ser corrigido. 
    return render(request, 'authors/pages/register_view.html', context={ 
        'form': form,
        'form_action': reverse('authors:register_create')
    }) 

def register_create(request): # POST 
    if not request.POST:
        raise Http404

    POST = request.POST # 1- Pegou os dados 
    request.session['register_form_data'] = POST # 2- Registrou na sessão 'register_form_data'
    form = RegisterForm(POST) # 3- É usado para validar e processar os dados enviados pelo usuário. 

    if form.is_valid(): # Se ele for valido...
        user = form.save(commit=False) # armazena os dados na varável (user) para ser criptografada. 
        user.set_password(user.password) # Criptografar a senha para não ver a senha no banco de dados
        user.save() # Salvar no banco de dados

        messages.success(request, 'Your user is created. Please log in') # Mensagem de sucesso.
        del(request.session['register_form_data']) # Vai apagar os dados da sessão. 

        return redirect('authors:login') 

    return redirect('authors:register')

def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', context={
        'form':form,
        'form_action': reverse('authors:login_create')
    })

def login_create(request):
    if not request.POST:
        raise Http404
    
    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )

        if authenticated_user is not None:
            messages.success(request, 'You are logged in')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Error to validate form data')
    
    return redirect(reverse('authors:dashboard'))

@login_required(login_url='authors:login', redirect_field_name='next') # Esse decorador diz que só vai poder executar a função caso o usuário esteja logado.
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))
    
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))

@login_required(login_url='authors:login', redirect_field_name='next') # Esse decorador diz que só vai poder executar a função caso o usuário esteja logado.
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )

    return render(request, 'authors/pages/dashboard.html', context={
        'recipes': recipes,
        'dashboard': True
    })

@login_required(login_url='authors:login', redirect_field_name='next') # Esse decorador diz que só vai poder executar a função caso o usuário esteja logado.
def dashboard_recipe_new(request):
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.slug = recipe.title

        base_slug = slugify(recipe.title)
        slug = base_slug
        count = 1

        # Garantindo unicidade do slug
        while Recipe.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        recipe.slug = slug

        recipe.save()

        messages.success(request, 'Your recipe has been save succesfully')
        return redirect(
            reverse('authors:dashboard')
        )

    return render(request, 'authors/pages/dashboard_recipe.html', context={
        'form': form,
        'form_action':reverse('authors:dashboard_recipe_new')
    })

@login_required(login_url='authors:login', redirect_field_name='next') # Esse decorador diz que só vai poder executar a função caso o usuário esteja logado.
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.get(
        is_published=False,
        author=request.user,
        pk=id
    )

    if not recipe:
        raise Http404

    form = AuthorRecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.slug = recipe.title.replace(' ', '-').strip()

        base_slug = slugify(recipe.title)
        slug = base_slug
        count = 1

        # Garantindo unicidade do slug
        while Recipe.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        recipe.slug = slug

        recipe.save()

        messages.success(request, 'Your form has been saved successfully')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id, )))

    
    return render(request, 'authors/pages/dashboard_recipe.html', context={
        'form':form,
        'recipe':recipe
    })

@login_required(login_url='authors:login', redirect_field_name='next') # Esse decorador diz que só vai poder executar a função caso o usuário esteja logado.
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404
    
    POST = request.POST
    id = POST.get('id')
    
    
    recipe = Recipe.objects.get(
        is_published=False,
        author=request.user,
        pk=id
    )

    if not recipe:
        raise Http404

    recipe.delete()

    messages.success(request, 'Your recipe has been successfully deleted')
    return redirect(reverse('authors:dashboard'))