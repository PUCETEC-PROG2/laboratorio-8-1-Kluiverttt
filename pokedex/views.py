from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from .models import Pokemon, Trainer
from pokedex.forms import PokemonForm, TrainerForm

def index(request):
    pokemons = Pokemon.objects.order_by('type')
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'pokemons': pokemons}, request))

def pokemon(request):
    pokemons = Pokemon.objects.order_by('type')
    template = loader.get_template('pokemon.html')
    return HttpResponse(template.render({'pokemons': pokemons}, request))

def trainer(request):
    trainers = Trainer.objects.order_by('first_name')
    template = loader.get_template('trainer.html')
    return HttpResponse(template.render({'trainers': trainers}, request))

def display_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(pk = pokemon_id)
    template = loader.get_template('display_pokemon.html')
    context = {
        'pokemon': pokemon
    }
    return HttpResponse(template.render(context, request))

def display_trainer(request, trainer_id):
    trainer = Trainer.objects.get(pk = trainer_id)
    template = loader.get_template('display_trainer.html')
    context = {
        'trainer': trainer
    }
    return HttpResponse(template.render(context, request))

@login_required
def add_pokemon(request):
    if request.method == 'POST':
        form = PokemonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pokedex:index')
    else:
        form = PokemonForm()

    return render(request, 'pokemon_form.html', {'form':form})


class CustomLoginView(LoginView):
    template_name = "login.html"

@login_required
def edit_pokemon(request, id):
    pokemon = get_object_or_404(Pokemon, pk = id)
    if request.method == 'POST':
        form = PokemonForm(request.POST, request.FILES, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect('pokedex:pokemon')
    else:
        form = PokemonForm(instance=pokemon)

    return render(request, 'pokemon_form.html', {'form':form})

@login_required
def delete_pokemon(requeest, id):
    pokemon = get_object_or_404(Pokemon, pk = id)
    pokemon.delete()
    return redirect("pokedex:index")

@login_required
def add_trainer(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pokedex:trainer')
    else:
        form = TrainerForm()

    return render(request, 'trainer_form.html', {'form':form})

@login_required
def edit_trainer(request, id):
    trainer = get_object_or_404(Trainer, pk = id)
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect('pokedex:trainer')
    else:
        form = TrainerForm(instance=trainer)

    return render(request, 'trainer_form.html', {'form':form})

@login_required
def delete_trainer(request, id):
    trainer = get_object_or_404(Trainer, pk = id)
    trainer.delete()
    return redirect("pokedex:trainer")