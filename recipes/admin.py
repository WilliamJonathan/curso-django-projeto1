from django.contrib import admin

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    ...

# maineira mais curta de registrar um model


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...


# maneira com mais passos de registrar um model
admin.site.register(Category, CategoryAdmin)
