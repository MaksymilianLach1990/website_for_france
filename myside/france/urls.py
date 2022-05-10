from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='france'),

    path('scenes-list', views.scenes_list, name='scenes-list'),
    path('add-scenes', views.add_scenes, name='add-scenes'),
    path('edit-scenes/<int:scene_id>', views.edit_scenes, name='edit-scenes'),
    path('delete-scenes/<int:scene_id>', views.delete_scenes, name='delete-scenes'),

    path('dialog/<int:scene_id>', views.dialog, name='dialog'),
    path('edit-dialog/<int:scene_id>', views.edit_dialog, name='edit-dialog'),
    path('add-phrase/<int:scene_id>', views.add_phrase, name='add-phrase'),
    path('edit-phrase/<int:scene_id>/<int:phrase_order>', views.edit_phrase, name='edit-phrase'),
    path('delete-phrase/<int:scene_id>/<int:phrase_id>', views.delete_phrase, name='delete-phrase'),
    path('phrase-order-up/<int:scene_id>/<int:phrase_order>', views.phrase_order_up, name='phrase-order-up'),
    path('phrase-order-down/<int:scene_id>/<int:phrase_order>', views.phrase_order_down, name='phrase-order-down'),

    path('dictionary', views.dictionary, name='dictionary'),
    path('add-word/<int:scene_id>', views.add_word, name='add-word'),
    path('edit-word/<int:word_id>', views.edit_word, name='edit-word'),
    path('delete-word/<int:word_id>', views.delete_word, name='delete-word'),
]