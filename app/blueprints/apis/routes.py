from app.blueprints.apis import apis
import requests
from flask_login import login_required

from flask import current_app,render_template, redirect, url_for
from app.blueprints.apis.forms import PokedexForm
from flask import render_template, redirect, url_for, flash

def pokemon_func(data_):
    pokemons =[]
    for pokemon in (data_):
        pokemon_ = requests.get(pokemon['url']).json()
        name = pokemon_['name'].capitalize()
        id = pokemon_["id"]
        if len(pokemon_["types"]) == 1:
            type_ = [pokemon_["types"][0]["type"]["name"].capitalize() ]
        else:
            type_ = [pokemon_["types"][0]["type"]["name"].capitalize() ,pokemon_["types"][1]["type"]["name"].capitalize() ]

        weight = pokemon_["weight"]
        sprite = pokemon_["sprites"]["front_default"]
        poke = [id,name ,type_,weight,sprite]
        pokemons.append(poke)
    return pokemons

@apis.route('/pokedex', methods=['GET'])
@login_required
def pokedex():
    data = requests.get('https://pokeapi.co/api/v2/pokemon').json()
    data_ =data['results']
    #print(data)

    pokemons = pokemon_func(data_)
    context = {
        
        'pokemons':pokemons
    }
    return render_template('pokedex.html',**context)

@apis.route('/pokedex/2', methods=['GET'])
@login_required
def pokedex2():
    
    data = requests.get('https://pokeapi.co/api/v2/pokemon?offset=20&limit=20').json()
    data_ =data['results']
    pokemons = pokemon_func(data_)

    
    context = {
        'pokemons':pokemons
    }
    return render_template('2.html',**context)


@apis.route('/pokedex/3', methods=['GET'])
@login_required
def pokedex3():
    
    data = requests.get('https://pokeapi.co/api/v2/pokemon?offset=40&limit=20').json()
    data_ =data['results']
    pokemons = pokemon_func(data_)

    
    context = {
        'pokemons':pokemons
    }
    return render_template('3.html',**context)


@apis.route('/ergast')
@login_required
def ergast():
    data = requests.get('https://ergast.com/api/f1/2008/5/driverStandings.json').json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    context = {
        'data':data
    }
    return render_template('ergast.html',**context)

