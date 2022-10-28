from collections import defaultdict

from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from tag.models import Tag


class Category(models.Model):
    name = models.CharField(max_length=65, verbose_name='nome')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Recipe(models.Model):
    title = models.CharField(max_length=65, verbose_name='titulo')
    description = models.CharField(max_length=165, verbose_name='descrição')
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField(verbose_name='tempo de preparação')
    preparation_time_unit = models.CharField(
        max_length=65, verbose_name='unidade de tempo de preparação')
    servings = models.IntegerField(verbose_name='porções')
    servings_unit = models.CharField(
        max_length=65, verbose_name='unidade de porções')
    preparation_steps = models.TextField(verbose_name='etapas de preparação')
    preparation_steps_is_html = models.BooleanField(
        default=False, verbose_name='etapas de preparação é html')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='criado em')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='atualizado em')
    is_published = models.BooleanField(
        default=False, verbose_name='Está publicado')
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', verbose_name='imagem')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None,
        verbose_name='categoria'
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name='autor'
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Encontrei receitas com o mesmo título'
                )

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'
