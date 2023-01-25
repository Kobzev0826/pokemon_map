from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.CharField('Название покемона', max_length=200)