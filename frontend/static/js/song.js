// static/js/song.js

document.addEventListener('DOMContentLoaded', function() {
    // Rating System
    const stars = document.querySelectorAll('.star');
    stars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = this.dataset.value;
            // Send rating to the server
            console.log(`Rated ${rating} stars`);
        });
    });

    // Comment Submission
    document.getElementById('addComment').addEventListener('click', function() {
        const commentInput = document.getElementById('commentInput');
        const commentText = commentInput.value;
        if (commentText) {
            // Send comment to the server
            console.log(`Comment added: ${commentText}`);
            commentInput.value = '';
        }
    });

    // Simulate Progress Bar
    const progressBar = document.getElementById('progressBar');
    let width = 0;
    const interval = setInterval(() => {
        if (width >= 100) {
            clearInterval(interval);
        } else {
            width++;
            progressBar.style.width = `${width}%`;
            progressBar.setAttribute('aria-valuenow', width);
        }
    }, 1000);
});
