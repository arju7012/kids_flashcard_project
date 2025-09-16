# kids_flashcard_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')), # Include URLs from the core app for the homepage
    path('flashcards/', include('flashcards.urls')), # Include URLs from the flashcards app
    path('users/', include('users.urls')),
]

# This is important for serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)