// flashcards/static/flashcards/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    // --- Get all the elements we need from the page ---
    const card = document.getElementById('flashcard');
    const flipButton = document.getElementById('flip-button');
    const frontAudioButton = document.getElementById('front-audio-button');
    const frontAudio = document.getElementById('front-audio');
    const backVideo = document.getElementById('back-video');
    
    // Get the button containers
    const answerButtons = document.getElementById('answer-buttons');
    const pageNavigation = document.getElementById('page-navigation');

    // --- Automatically play the front audio ONCE when the card loads ---
    if (frontAudio) {
        setTimeout(() => {
            frontAudio.play().catch(error => {
                console.log("Autoplay was prevented by the browser.");
            });
        }, 200);
    }

    // --- Flip the card when the "Show Answer" button is clicked ---
    if (flipButton) {
        flipButton.addEventListener('click', function() {
            card.classList.toggle('is-flipped');
        });
    }

    // --- Play the front audio AGAIN when the icon is clicked ---
    if (frontAudioButton) {
        frontAudioButton.addEventListener('click', function(event) {
            event.stopPropagation(); 
            frontAudio.play();
        });
    }

    // --- Handle UI changes and video playback after the flip animation ---
    if (card) {
        card.addEventListener('transitionend', () => {
            // When the card is flipped to the BACK
            if (card.classList.contains('is-flipped')) {
                if (pageNavigation) pageNavigation.classList.add('d-none'); // Hide Previous/Finish
                if (answerButtons) answerButtons.classList.remove('d-none'); // Show Answer Buttons
                if (backVideo) backVideo.play();
            } else {
                // When the card is flipped back to the FRONT
                if (answerButtons) answerButtons.classList.add('d-none'); // Hide Answer Buttons
                if (pageNavigation) pageNavigation.classList.remove('d-none'); // Show Previous/Finish
                if (backVideo) {
                    backVideo.pause();
                    backVideo.currentTime = 0;
                }
            }
        });
    }
});