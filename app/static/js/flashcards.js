document.querySelectorAll('.flashcard').forEach(card => {
    card.addEventListener('click', function() {
        this.querySelector('.card-content').classList.toggle('is-flipped');
    });
});

// Adjust text size dynamically based on content length
document.querySelectorAll('.card-text').forEach(text => {
    const length = text.innerHTML.length;

    if (length > 100) {
        text.style.fontSize = '12px'; // Smaller text for very long content
    } else if (length > 60) {
        text.style.fontSize = '14px'; // Slightly larger for medium-long content
    } else if (length > 30) {
        text.style.fontSize = '16px'; // Standard size for moderate length
    } else {
        text.style.fontSize = '20px'; // Larger text for short content
    }
});