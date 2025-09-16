// flashcards/static/flashcards/js/script.js

document.addEventListener('DOMContentLoaded', function() {
    // --- Get all the elements we need from the page ---
    const card = document.getElementById('flashcard');
    const flipButton = document.getElementById('flip-button');
    const backVideo = document.getElementById('back-video');
    const frontAudioButton = document.getElementById('front-audio-button');
    const frontAudio = document.getElementById('front-audio');

    // --- Automatically play the front audio ONCE when the card loads ---
    if (frontAudio) {
        // A short delay can help ensure the browser is ready to play.
        setTimeout(() => {
            frontAudio.play().catch(error => {
                // This catch block handles cases where the browser blocks autoplay.
                console.log("Autoplay was prevented by the browser.");
            });
        }, 200);
    }

    // --- Flip the card when the button is clicked ---
    if (flipButton) {
        flipButton.addEventListener('click', function() {
            card.classList.toggle('is-flipped');
        });
    }

    // --- Play the front audio AGAIN when the icon is clicked ---
    if (frontAudioButton) {
        frontAudioButton.addEventListener('click', function(event) {
            // Stop the click from affecting other elements
            event.stopPropagation(); 
            frontAudio.play();
        });
    }

    // --- Handle video playback on the back of the card ---
    if (card && backVideo) {
        card.addEventListener('transitionend', () => {
            if (card.classList.contains('is-flipped')) {
                // Play the video when flipped to the back
                backVideo.play();
            } else {
                // Pause and rewind if flipped back to the front
                backVideo.pause();
                backVideo.currentTime = 0;
            }
        });
    }
});