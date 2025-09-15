# flashcards/models.py

from django.db import models

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