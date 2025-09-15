# flashcards/admin.py

from django.contrib import admin
from .models import Deck, Card

class CardInline(admin.TabularInline):
    model = Card
    extra = 1
    # Add new fields to the compact view
    fields = ('front_text', 'front_image', 'front_audio', 'back_video', 'back_text')

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    inlines = [CardInline]

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    # Add front_text to the main list display
    list_display = ('front_text', 'deck', 'front_image')
    list_filter = ('deck',)