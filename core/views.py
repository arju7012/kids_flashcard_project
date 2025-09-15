# core/views.py

from django.shortcuts import render
from flashcards.models import Deck # Import the Deck model from the flashcards app

def home_view(request):
    # Fetch all the decks to display on the homepage
    decks = Deck.objects.all()
    context = {
        'decks': decks
    }
    return render(request, 'core/home.html', context)