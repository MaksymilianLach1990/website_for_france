from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('sing-up', views.sing_up, name='sing-up'),
    path('create-post', views.create_post, name='create-post'),
    
]
