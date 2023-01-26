from django.contrib import admin

# Register your models here.
from .models import Category, Anime

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]
    search_fields = ['name']

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'category',
        'compania',
        'date'
    ]
    search_fields = ['name']
    list_filter = [
        'category',
        'date',
        'compania'
    ]