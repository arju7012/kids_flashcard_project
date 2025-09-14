from django.shortcuts import render

def flashcard_home(request):
    return render(request, 'flashcards/flashcard.html')
