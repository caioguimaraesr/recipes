from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse

def register_view(request): # GET
    register_form_data = request.session.get('register_form_data', None) # 4- Vai armazenas os dados na variável 'register_form_data', caso não tenha nada, será None
    form = RegisterForm(register_form_data) # 5- Caso for for None (Deu tudo certo com a outra sessão) inciará sem nada, se contiver dados na sessão será exibido os erros para ser corrigido. 
    return render(request, 'authors/pages/register_view.html', context={ 
        'form': form,
        'form_action': reverse('authors:create')
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

    return redirect('authors:register')