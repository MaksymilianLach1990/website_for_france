from django.contrib import admin
from .models import Scenes, Phrase, Word

# Register your models here.

@admin.register(Scenes)
class EventAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'created_at', 'scene_image')
    list_display = ('name', 'description', 'created_at')
    ordering = ('name', 'created_at')


@admin.register(Phrase)
class EventAdmin(admin.ModelAdmin):
    fields = ('scenes', 'character_name', 'sentence', 'order', 'created_at')
    list_display = ('scenes', 'character_name', 'sentence', 'order', 'created_at')
    ordering = ('scenes', 'created_at')


@admin.register(Word)
class EventAdmin(admin.ModelAdmin):
    fields = ('scenes', 'word_pl', 'word_fr', 'description', 'phonetic')
    list_display = ('word_pl', 'word_fr', 'description', 'phonetic')
    ordering = ('word_pl', 'word_fr')
