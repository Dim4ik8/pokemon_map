from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    title = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=True, blank=True)
    lat = models.FloatField()
    lon = models.FloatField()

