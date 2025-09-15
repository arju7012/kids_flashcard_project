# flashcards/urls.py

from django.urls import path
from .views import learn_deck_view

urlpatterns = [
    # Example URL: /flashcards/deck/1/
    path('deck/<int:deck_id>/', learn_deck_view, name='learn_deck'),
]