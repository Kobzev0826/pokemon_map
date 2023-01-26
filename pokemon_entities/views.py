import folium
import json

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import Pokemon, PokemonEntity
from django.utils import timezone

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
    # with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
    #     pokemons = json.load(database)['pokemons']

    pokemons = Pokemon.objects.all()
    now = timezone.localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in PokemonEntity.objects.filter(pokemon__id=pokemon.id, appeared_at__lt=now,
                                                           disappeared_at__gt=now):
            add_pokemon(
                folium_map, pokemon_entity.latitude,
                pokemon_entity.longitude,
                pokemon.photo.path
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.photo.url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    # with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
    #     pokemons = json.load(database)['pokemons']
    #
    # for pokemon in pokemons:
    #     if pokemon['pokemon_id'] == int(pokemon_id):
    #         requested_pokemon = pokemon
    #         break
    # else:
    #     return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except (MultipleObjectsReturned, ObjectDoesNotExist):
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')


    now = timezone.localtime()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon = {
        'title': requested_pokemon.title,
        'img_url': request.build_absolute_uri(requested_pokemon.photo.url),
        'description': requested_pokemon.description,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
    }
    for pokemon_entity in PokemonEntity.objects.filter(pokemon__id=requested_pokemon.id, appeared_at__lt=now,
                                                           disappeared_at__gt=now):
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(requested_pokemon.photo.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
