from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField('Название покемона', max_length=200)
    photo = models.ImageField('Фото покемона', upload_to='pokemons', null=True, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, verbose_name='Модель покемона',
        related_name='pokemon_info',)
    appeared_at = models.DateTimeField("Покемон появляется",null=True, blank=True)
    disappeared_at = models.DateTimeField("Покемон исчезает ", null=True, blank = True)