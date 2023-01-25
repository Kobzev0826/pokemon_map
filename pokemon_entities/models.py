from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField('Название покемона', max_length=200)
    photo = models.ImageField('Фото покемона', upload_to='pokemons', null=True, blank=True)

    def __str__(self):
        return self.title