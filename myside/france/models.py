from django.db import models
import datetime

# Create your models here.

class Scenes(models.Model):
    class Meta:
        ordering = ('name', 'created_at')

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=300)
    scene_image = models.URLField(null=True, blank=True)
    created_at = models.DateField(default=datetime.date.today, db_index=True)

    def __str__(self):
        return f'{self.name}'


class Phrase(models.Model):
    class Meta:
        ordering = ('scenes', 'order')

    scenes = models.ForeignKey(Scenes, models.CASCADE)
    character_name = models.CharField(max_length=100)
    sentence = models.TextField(max_length=400)
    order = models.IntegerField()
    created_at = models.DateField(default=datetime.date.today, db_index=True)

    def __str__(self):
        return f'{self.scenes} - {self.order} - {self.created_at}'

    def go_up(self, phrase_num, scene_num):

        phrase_up = Phrase.objects.filter(scenes=scene_num, order=phrase_num).first()
        phrase_up.order = 0
        phrase_up.save()
        phrase_down = Phrase.objects.filter(scenes=scene_num, order=(phrase_num-1)).first()
        phrase_down.order = phrase_num
        phrase_down.save()
        phrase_new = Phrase.objects.filter(scenes=scene_num, order=0).first()
        phrase_new.order = phrase_num-1
        phrase_new.save()

    def go_down(self, phrase_num, scene_num):
        
        phrase_down = Phrase.objects.filter(scenes=scene_num, order=phrase_num).first()
        phrase_down.order = 0
        phrase_down.save()
        phrase_up = Phrase.objects.filter(scenes=scene_num, order=(phrase_num+1)).first()
        phrase_up.order = phrase_num
        phrase_up.save()
        phrase_new = Phrase.objects.filter(scenes=scene_num, order=0).first()
        phrase_new.order = phrase_num+1
        phrase_new.save()
    

class Word(models.Model):
    class Meta:
        ordering = ('word_pl', 'word_fr')

    scenes = models.ForeignKey(Scenes, models.CASCADE)
    word_pl = models.CharField(max_length=100)
    word_fr = models.CharField(max_length=100)
    description = models.TextField(max_length=400, blank=True)
    phonetic = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.word_pl} - {self.word_fr}'
