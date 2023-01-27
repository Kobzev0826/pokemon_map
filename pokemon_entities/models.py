from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField('Название покемона', max_length=200)
    photo = models.ImageField('Фото покемона', upload_to='pokemons', null=True, blank=True)
    description = models.CharField('Описание покемона', max_length=2000, null=True, blank=True)
    title_en = models.CharField('Название на английском',  max_length=200, null=True, blank = True)
    title_jp = models.CharField('Название на японском', max_length=200, null=True, blank = True)
    previous_evolution = models.ForeignKey(
        "self", on_delete=models.CASCADE,null=True, blank=True,
        related_name='pokemon_evolution_previous', verbose_name="Из кого эволюционирует")

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
    level = models.IntegerField("Уровень покемона", null=True, blank=True, default=5)
    health = models.IntegerField('Здоровье покемона', null=True, blank=True,default=5)
    strength = models.IntegerField('Сила покемона', null=True, blank=True,default=5)
    defence = models.IntegerField("Защита покемона", null=True, blank=True,default=5)
    stamina = models.IntegerField("Выносливость покемона", null=True, blank=True,default=5)