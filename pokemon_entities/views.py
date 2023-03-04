import folium

from django.shortcuts import render
from django.utils.timezone import localtime

from .models import *

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        pokemon = Pokemon.objects.get(title=pokemon_entity.title)
        if (pokemon_entity.appeared_at < localtime() and pokemon_entity.disappeared_at > localtime()):
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                f'media/{pokemon.image}',
            )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': f'../media/{pokemon.image}',
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    previous_evolution = {}
    if requested_pokemon.previous_evolution:
        previous_evolution = {
            'pokemon_id': requested_pokemon.previous_evolution.id,
            'title_ru': requested_pokemon.previous_evolution.title,
            'img_url': f'../../media/{requested_pokemon.previous_evolution.image}',
        }

    pokemon = {
        'title_ru': requested_pokemon.title,
        'img_url': f'../../media/{requested_pokemon.image}',
        'description': requested_pokemon.description,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'previous_evolution': previous_evolution,
    }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(title=requested_pokemon.id)
    for pokemon_entity in pokemon_entities:
        if (pokemon_entity.appeared_at < localtime() and pokemon_entity.disappeared_at > localtime()):
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                f'media/{requested_pokemon.image}',
            )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
