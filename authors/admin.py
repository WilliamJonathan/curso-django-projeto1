from django.contrib import admin

from authors.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['author', ]
    list_display_links = ['author', ]
