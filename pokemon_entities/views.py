import folium
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Pokemon, PokemonEntity

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
    pokemons = Pokemon.objects.all()
    now = timezone.localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in PokemonEntity.objects.filter(pokemon__id=pokemon.id, appeared_at__lt=now,
                                                           disappeared_at__gt=now):
            image = pokemon_entity.pokemon.photo.url if pokemon_entity.pokemon.photo else DEFAULT_IMAGE_URL
            add_pokemon(
                folium_map, pokemon_entity.latitude,
                pokemon_entity.longitude,
                request.build_absolute_uri(image)
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.photo.url if pokemon.photo else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):

    requested_pokemon = get_object_or_404(Pokemon,id=pokemon_id)

    now = timezone.localtime()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    next_evo_pokemon = requested_pokemon.pokemon_evolution_previous.first()
    next_evolution = None
    if next_evo_pokemon:
        next_evolution = {
            "title_ru": next_evo_pokemon.title,
            "pokemon_id": next_evo_pokemon.id,
            "img_url": next_evo_pokemon.photo.url if next_evo_pokemon.photo else DEFAULT_IMAGE_URL
        }

    previous_evolution = None
    if requested_pokemon.previous_evolution:
        previous_evolution = {
            "title_ru": requested_pokemon.previous_evolution.title,
            "pokemon_id": requested_pokemon.previous_evolution.id,
            "img_url": requested_pokemon.previous_evolution.photo.url
            if requested_pokemon.previous_evolution.photo else DEFAULT_IMAGE_URL
        }



    image = requested_pokemon.photo.url if requested_pokemon.photo else DEFAULT_IMAGE_URL
    pokemon = {
        'title': requested_pokemon.title,
        'img_url': request.build_absolute_uri(image),
        'description': requested_pokemon.description,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "next_evolution": next_evolution,
        "previous_evolution": previous_evolution
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
