from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField()
    description = models.TextField(default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="title",
        null=True, blank=True)

    @property
    def rating(self):
        return 0

    @property
    def genre(self):
        queryset = GenreTitle.objects.filter(title_id=self.id)
        return Genre.objects.filter(id__in=queryset)

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
                name='unique_name_owner'
            )
        ]

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'
