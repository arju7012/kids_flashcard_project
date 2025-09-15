// flashcards/static/flashcards/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    // --- Card Flipping Logic ---
    const card = document.getElementById('flashcard');
    const flipButton = document.getElementById('flip-button');

    if (card && flipButton) {
        flipButton.addEventListener('click', function() {
            // This is the line that makes the card flip.
            // 'toggle' is better than 'add' as it lets you flip it back.
            card.classList.toggle('is-flipped');
        });
    }

    // --- Audio Playing Logic ---
    const backVideo = document.getElementById('back-video');
    const frontAudioButton = document.getElementById('front-audio-button');
    const frontAudio = document.getElementById('front-audio');

    if (frontAudioButton && frontAudio) {
        frontAudioButton.addEventListener('click', function(event) {
            // Stop the click from bubbling up to other elements
            event.stopPropagation(); 
            frontAudio.play();
        });
    }

    // Autoplay back video when flip is complete
    if (card && backVideo) {
        card.addEventListener('transitionend', () => {
            if (card.classList.contains('is-flipped')) {
                // Play the video only when flipped to the back
                backVideo.play();
            } else {
                // Pause and rewind if flipped back to the front
                backVideo.pause();
                backVideo.currentTime = 0;
            }
        });
    }
});