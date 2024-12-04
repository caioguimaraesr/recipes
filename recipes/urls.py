from django.urls import path
from recipes import views

urlpatterns = [
    path('', views.home), #/home
    path('contato/', views.contato), #/sobre
    path('sobre/', views.sobre) #/contato
]