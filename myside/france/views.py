from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required

from .forms import ScenesCreateForm, PhraseCreateForm, WordCreateForm, SearchWordForm
from .models import Scenes, Phrase, Word


# Create your views here.

# Home page section
# Everyone can see
def home(request):

    scenes_list = Scenes.objects.all()

    context = {
        'scenes_list': scenes_list,
        }

    return render(request, 'france/home.html', context)

# Scenes section
@login_required(login_url="/login")
def scenes_list(request):

    scenes_list = Scenes.objects.all()

    context = {
        'scenes_list': scenes_list,
        'message': 'Nie ma scenek!',
        }

    return render(request, 'france/scenes_list.html', context)

@login_required(login_url="/login")
@permission_required("france.add_scenes", login_url="/france", raise_exception=True)
def add_scenes(request):

    if request.method == 'POST':
        form = ScenesCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            scene_id = Scenes.objects.filter(name=request.POST['name']).first()
            return redirect(f'/france/dialog/{scene_id.id}')
        else:
            return redirect("/france/add-scenes")

    context = {
        'title': "Dodaj Scenkę",
        'form': ScenesCreateForm,
        }
    return render(request, 'france/edit_scenes.html', context)

# Everyone can see
def dialog(request, scene_id):
    
    situation = Scenes.objects.get(id=scene_id)
    dialog_list = Phrase.objects.filter(scenes=scene_id).order_by('order')

    context = {
        'dialog_list': dialog_list,
        'situation': situation,
        }

    return render(request, 'france/dialog.html', context)



# Edit Scenes section
@login_required(login_url="/login")
@permission_required("france.change_scenes", login_url="/france", raise_exception=True)
def edit_scenes(request, scene_id):

    scene = Scenes.objects.get(id=scene_id)
    
    if request.method == 'POST':
        scene.name = request.POST['name']
        scene.description = request.POST['description'] 
        scene.save()

        return redirect(f'/france/edit-dialog/{scene_id}')

    form = ScenesCreateForm(instance=scene)

    context ={
        'title': 'Edytuj Scenkę',
        'form': form,
        }

    return render(request, 'france/edit_scenes.html', context)

@login_required(login_url="/login")
@permission_required("france.delete_scenes", login_url="/france", raise_exception=True)
def delete_scenes(request, scene_id):

    scene = Scenes.objects.get(id=scene_id)
    scene.delete()

    return redirect('/france/scenes-list')

# Edit Dialog section
@login_required(login_url="/login")
@permission_required("france.change_scenes", login_url="/france", raise_exception=True)
def edit_dialog(request, scene_id):

    test = "Message"

    situation = Scenes.objects.get(id=scene_id)
    dialog_list = Phrase.objects.filter(scenes=scene_id).order_by('order')

    context = {
        'dialog_list': dialog_list,
        'situation': situation,
        'test': test,
        }

    return render(request, 'france/edit_dialog.html', context)


@login_required(login_url="/login")
@permission_required("france.add_phrase", login_url="/france", raise_exception=True)
def add_phrase(request, scene_id):

    if request.method == 'POST':
        scene = Scenes.objects.get(id=scene_id)
        name = request.POST['character_name']
        sentence = request.POST['sentence']

        phrases = Phrase.objects.filter(scenes=scene_id).all()

        if len(phrases) == 0:
            order_num = 1
        else:
            order_max = [phrase.order for phrase in phrases]
            order_num = max(order_max) + 1

        form = Phrase(scenes=scene, character_name=name, sentence=sentence, order=order_num)
        
        form.save()

        return redirect(f'/france/edit-dialog/{scene_id}')

    context = {
        'title': 'Dodaj wypowiedź',
        'form': PhraseCreateForm,
        }
    return render(request, 'france/edit_phrase.html', context)

@login_required(login_url="/login")
@permission_required("france.change_phrase", login_url="/france", raise_exception=True)
def edit_phrase(request, scene_id, phrase_order):

    phrase = Phrase.objects.get(scenes=scene_id, order=phrase_order)

    if request.method == 'POST':
        phrase.character_name = request.POST['character_name']
        phrase.sentence = request.POST['sentence']

        phrase.save()

        return redirect(f'/france/edit-dialog/{scene_id}')
        

    context = {
        'title': 'Edytuj wypowiedź',
        'form': PhraseCreateForm(instance=phrase),
        }
    return render(request, 'france/edit_phrase.html', context)

@login_required(login_url="/login")
@permission_required("france.delete_phrase", login_url="/france", raise_exception=True)
def delete_phrase(request, scene_id, phrase_id):

    phrase = Phrase.objects.get(id=phrase_id)
    phrase.delete()

    return redirect(f'/france/edit-dialog/{scene_id}')

@login_required(login_url="/login")
@permission_required("france.change_phrase", login_url="/france", raise_exception=True)
def phrase_order_up(request, scene_id, phrase_order):
    if phrase_order == 1:
        return redirect(f'/france/edit-dialog/{scene_id}')

    Phrase().go_up(phrase_order, scene_id)
    
    return redirect(f'/france/edit-dialog/{scene_id}')

@login_required(login_url="/login")
@permission_required("france.change_phrase", login_url="/france", raise_exception=True)
def phrase_order_down( request, phrase_order, scene_id):
    if phrase_order == max([phrase.order for phrase in Phrase.objects.filter(scenes=scene_id).all()]):
        return redirect(f'/france/edit-dialog/{scene_id}')

    Phrase().go_down(scene_id, phrase_order)

    return redirect(f'/france/edit-dialog/{scene_id}')

# Dictionary section
# Everyone can see
def dictionary(request):

    search_word = ''

    try:
        if request.method == 'POST':
            if request.POST['language'] == 'fr':
                word = Word.objects.get(word_fr=request.POST['word'].lower())
                search_word = {
                    'word': word.word_fr,
                    'translate': word.word_pl,
                    'phonetic': word.phonetic,
                    'description': word.description,
                }
            if request.POST['language'] == 'pl':
                word = Word.objects.get(word_pl=request.POST['word'].lower())
                search_word = {
                    'word': word.word_pl,
                    'translate': word.word_fr,
                    'phonetic': word.phonetic,
                    'description': word.description,
                }
    except:
        search_word = {'description': "Sorry, something went wrong! Try again."}

    context = {
        'dictionary': Word.objects.all(),
        'form': SearchWordForm,
        'search_word': search_word,
        }

    return render(request, 'france/dictionary.html', context)

@login_required(login_url="/login")
@permission_required("france.add_word", login_url="/france", raise_exception=True)
def add_word(request, scene_id):

    if request.method == 'POST':
        form = WordCreateForm(request.POST)
        if form.is_valid():
            word = form.save(commit=False)
            word.word_pl = word.word_pl.lower()
            word.word_fr = word.word_fr.lower()
            word.save()
        if scene_id == 0:
            return redirect('/france/dictionary')
        else:
            return redirect(f'/france/edit-dialog/{scene_id}')
    if scene_id == 0:
        form = WordCreateForm
    else:
        scene = Scenes.objects.get(id=scene_id)
        form = WordCreateForm(instance=Word(scenes=scene))
    
    context = {
        'title': 'Dodaj słowo',
        'form': form,
        }

    return render(request, 'france/edit_word.html', context)

@login_required(login_url="/login")
@permission_required("france.change_word", login_url="/france", raise_exception=True)
def edit_word(request, word_id):

    word = Word.objects.get(id=word_id)
    
    if request.method == 'POST':
        if request.POST['scenes'] == '':
            scene = ''
        else:
            scene = Scenes.objects.get(id=request.POST['scenes'])
        word.scenes = scene
        word.word_pl = request.POST['word_pl']
        word.word_fr = request.POST['word_fr']
        word.description = request.POST['description']
        word.phonetic = request.POST['phonetic']
        
        word.save()

        return redirect('/france/dictionary')

    form = WordCreateForm(instance=word)

    context ={
        'title': 'Edytuj słowo',
        'form': form,
        }

    return render(request, 'france/edit_word.html', context)

@login_required(login_url="/login")
@permission_required("france.delete_word", login_url="/france", raise_exception=True)
def delete_word(request, word_id):

    word = Word.objects.get(id=word_id)
    word.delete()

    return redirect('/france/dictionary')






