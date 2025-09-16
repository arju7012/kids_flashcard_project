# flashcards/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Deck, Card, UserProgress
from django.db.models import Q # Used for complex queries

@login_required # Ensures only logged-in users can access the learning deck
def learn_deck_view(request, deck_id):
    """
    This view is the core of the learning session.
    It intelligently fetches a queue of cards for the user, including:
    1. Cards that are due for review.
    2. A few new cards the user has never seen before.
    """
    deck = get_object_or_404(Deck, id=deck_id)
    user = request.user

    # --- Build the learning queue ---

    # 1. Get all cards that are DUE for review for this user in this deck.
    # We order by the review date to show the most overdue cards first.
    due_progress_items = UserProgress.objects.filter(
        user=user,
        card__deck=deck,
        next_review_date__lte=timezone.now()
    ).order_by('next_review_date')
    
    due_cards = [progress.card for progress in due_progress_items]

    # 2. Get a few NEW cards that the user has never reviewed before.
    # First, find the IDs of all cards the user *has* seen.
    seen_card_ids = UserProgress.objects.filter(user=user, card__deck=deck).values_list('card_id', flat=True)
    
    # Then, find cards in the deck that are NOT in the seen list.
    # We limit this to 5 new cards per session to avoid overwhelming the user.
    new_cards = deck.cards.exclude(id__in=seen_card_ids)[:5]

    # 3. Combine the lists: due cards are the priority, then new cards.
    learning_queue = due_cards + list(new_cards)

    # --- Pagination Logic ---
    # Show one card from the queue at a time.
    card_index = int(request.GET.get('card', 0))

    if not 0 <= card_index < len(learning_queue):
        # If the index is invalid or the queue is finished, reset.
        card_index = 0 

    current_card = learning_queue[card_index] if learning_queue else None
    
    context = {
        'deck': deck,
        'card': current_card,
        'queue_count': len(learning_queue),
        # Note: We no longer need prev/next index buttons, as the answer buttons handle navigation.
    }
    return render(request, 'flashcards/learn_item.html', context)


@login_required # Ensures only logged-in users can submit a review
def process_review_view(request, card_id, choice):
    """
    This view processes the user's answer ('again', 'hard', 'good', 'easy'),
    updates their progress, and redirects them to the next card.
    """
    # Get the specific card the user is reviewing.
    card = get_object_or_404(Card, id=card_id)
    
    # Get the UserProgress object for this user and card.
    # If it's the first time, a new progress object is created.
    progress, created = UserProgress.objects.get_or_create(user=request.user, card=card)
    
    # Call our algorithm in the model to update the progress.
    progress.process_review(choice)
    
    # Redirect the user back to the deck they were learning.
    # The learn_deck_view will automatically show them the next card in their queue.
    return redirect('learn_deck', deck_id=card.deck.id)