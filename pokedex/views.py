from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from pokedex.forms import PokemonForm
from .models import Pokemon
def index(request):
    pokemons = Pokemon.objects.order_by("type")
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'pokemons': pokemons}, request))

def pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(pk = pokemon_id) 
    template = loader.get_template('display_pokemon.html')
    context = {
        'pokemon': pokemon
    }
def add_pokemon(request):
    if request.method == 'POST':
        form = PokemonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pokedex:index')
    else:
        form = PokemonForm()
     
        
    return render(request,'add_pokemon.html',{'form':form}) 

class CustomLoginView(LoginView):
    template_name ='login.html'
    