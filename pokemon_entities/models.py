from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(verbose_name='Имя покемона', max_length=200)
    image = models.ImageField(verbose_name='Картинка покемона', null=True)
    description = models.TextField(verbose_name='Описание')
    title_en = models.CharField(
        verbose_name='Имя покемона по-английски',
        max_length=200,
        blank=True
    )
    title_jp = models.CharField(
        verbose_name='Имя покемона по-японски',
        max_length=200,
        blank=True
    )
    previous_evolution = models.ForeignKey(
        'self',
        related_name='next_evolutions',
        verbose_name='Из кого эволюционировал',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.PROTECT,
        verbose_name='Имя покемона',
        related_name='entities'
    )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(
        verbose_name='Время появления покемона',
        null=True,
        blank=True
    )
    disappeared_at = models.DateTimeField(
        verbose_name='Время исчезания покемона',
        null=True,
        blank=True
    )
    level = models.IntegerField(verbose_name='Уровень', null=True, blank=True)
    health = models.IntegerField(
        verbose_name='Здоровье',
        null=True, blank=True
    )
    strength = models.IntegerField(verbose_name='Сила', null=True, blank=True)
    defence = models.IntegerField(verbose_name='Защита', null=True, blank=True)
    stamina = models.IntegerField(
        verbose_name='Выносливость',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.pokemon}, появился(появится) " \
               f"{self.appeared_at.strftime('%d-%m-%Y %H:%M')}, " \
               f"исчез(исчезнет) " \
               f"{self.disappeared_at.strftime('%d-%m-%Y %H:%M')}"
