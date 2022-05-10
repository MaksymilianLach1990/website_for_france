from django import forms
from .models import Scenes, Phrase, Word

class ScenesCreateForm(forms.ModelForm):
    class Meta:
        model = Scenes
        fields = ('name', 'description', 'scene_image')
        labels = {
            'name': '',
            'description': '',
            'scene_image': '',
        }


class PhraseCreateForm(forms.ModelForm):
    class Meta:
        model = Phrase
        fields = ('character_name', 'sentence')
        labels = {
            'character_name': '',
            'sentence': '',
        }


class WordCreateForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ('scenes', 'word_pl', 'word_fr', 'description', 'phonetic')
        labels = {
            'scenes': '',
            'word_pl': '',
            'word_fr': '',
            'description': '',
            'phonetic': '',
        }

class SearchWordForm(forms.Form):

    CHOICES = (
        ('pl', 'polonais'),
        ('fr', 'français'),
    )

    word = forms.CharField(max_length=100)
    language = forms.ChoiceField(choices=CHOICES)
