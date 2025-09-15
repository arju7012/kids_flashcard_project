# flashcards/views.py

from django.shortcuts import render, get_object_or_404
from .models import Deck, Card

def learn_deck_view(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    cards = deck.cards.all() # Get all cards for this deck

    # Get the current card index from the URL query parameter, default to 0 (the first card)
    card_index = int(request.GET.get('card', 0))

    # Make sure the index is within the valid range
    if not 0 <= card_index < len(cards):
        card_index = 0 # Reset to first card if index is invalid

    current_card = cards[card_index] if cards else None

    # Calculate previous and next card indexes for navigation
    prev_card_index = card_index - 1 if card_index > 0 else None
    next_card_index = card_index + 1 if card_index < len(cards) - 1 else None

    context = {
        'deck': deck,
        'card': current_card,
        'prev_card_index': prev_card_index,
        'next_card_index': next_card_index,
        'is_last_card': next_card_index is None, # Flag to know if it's the last card
    }

    return render(request, 'flashcards/learn_item.html', context)