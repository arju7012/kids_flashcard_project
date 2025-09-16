# flashcards/models.py

from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, datetime


class Deck(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default='🧠')
    color = models.CharField(max_length=20, default='#6A1B9A')

    def __str__(self):
        return self.name

class Card(models.Model):
    deck = models.ForeignKey(Deck, related_name='cards', on_delete=models.CASCADE)
    
    # --- NEW & UPDATED FIELDS ---
    front_text = models.CharField(max_length=100) # e.g., "A"
    front_image = models.ImageField(upload_to='flashcard_images/fronts/')
    front_audio = models.FileField(upload_to='flashcard_sounds/fronts/', blank=True, null=True) # Optional sound
    
    back_video = models.FileField(upload_to='flashcard_videos/backs/')
    back_text = models.CharField(max_length=200, help_text="e.g., A is for Apple")

    def __str__(self):
        return f"Card for {self.front_text} (in {self.deck.name})"
    



class UserProgress(models.Model):
    """
    Stores the learning progress for a specific User on a specific Card.
    This is the core of the spaced repetition system.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    
    # The 'strength' of the user's memory for this card. Higher is better.
    mastery_level = models.IntegerField(default=0) 
    
    # The next date the user should review this card.
    next_review_date = models.DateTimeField(default=timezone.now)

    class Meta:
        # Ensures a user can only have one progress entry per card.
        unique_together = ('user', 'card')

    def __str__(self):
        return f"{self.user.username}'s progress on {self.card.front_text}"

    def process_review(self, choice):
        """
        This is our Spaced Repetition algorithm.
        It updates the mastery_level and next_review_date based on the user's choice.
        Choices: 'again', 'hard', 'good', 'easy'
        """
        # --- Handle "AGAIN" ---
        # The user forgot. Reset progress and show again soon.
        if choice == 'again':
            self.mastery_level = 0
            # Show this card again in 10 minutes for a quick re-test.
            self.next_review_date = timezone.now() + timedelta(minutes=10)
        
        else:
            # For any correct answer, we first check if the card was reviewed on time.
            # If it was late, we use the date it was *supposed* to be reviewed for the calculation.
            # This prevents overly long delays if a user misses a day.
            effective_date = min(self.next_review_date, timezone.now())

            # --- Handle "HARD" ---
            # User struggled. Small interval increase.
            if choice == 'hard':
                # Mastery level stays the same.
                # Interval is slightly longer than the last one.
                # We add a small base of 1 day to ensure it always moves forward.
                interval_days = (datetime.now(timezone.utc) - effective_date).days * 1.2 + 1
                self.next_review_date = timezone.now() + timedelta(days=interval_days)

            # --- Handle "GOOD" ---
            # This is the standard correct answer.
            elif choice == 'good':
                self.mastery_level += 1
                interval_days = 2 ** self.mastery_level
                self.next_review_date = timezone.now() + timedelta(days=interval_days)
            
            # --- Handle "EASY" ---
            # User knew it perfectly. Give them a bonus.
            elif choice == 'easy':
                self.mastery_level += 2 # Bonus level up
                # Give an extra multiplier to the interval.
                interval_days = (2 ** self.mastery_level) * 1.5 
                self.next_review_date = timezone.now() + timedelta(days=interval_days)
        
        # Save the updated progress to the database.
        self.save()