from django.urls import path
from . import views

urlpatterns = [
    path('', views.flashcard_home, name='flashcards_home'),
]
