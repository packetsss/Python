from django.contrib import admin
from . import models


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("title", "id", "status", "slug", "author")


admin.site.register(models.Post, AuthorAdmin)
admin.site.register(models.Category)
