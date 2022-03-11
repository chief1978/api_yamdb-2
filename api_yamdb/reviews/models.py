from datetime import date

from django.core.validators import MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(int(date.today().year)), ]
    )
    description = models.TextField(default='', null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="title",
        null=True, blank=True)

    genre = models.ManyToManyField(Genre, through='GenreTitle', blank=True)

    @property
    def rating(self):
        return 0

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="title",
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="genre",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'genre_id'],
                name='unique_title_genre'
            )
        ]

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'
