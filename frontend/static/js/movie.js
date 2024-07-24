// frontend/static/js/movie.js

document.addEventListener('DOMContentLoaded', () => {
    const playbackBar = document.querySelector('.playback-bar input[type="range"]'); 
    const currentTimeDisplay = document.getElementById('current-time');
    const totalTimeDisplay = document.getElementById('total-time');
    const commentForm = document.getElementById('comment-form');
    const commentsList = document.getElementById('comments-list');

    const stars = document.querySelectorAll('.stars label');
    stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            // Clear all stars
            stars.forEach(s => s.style.color = '#ccc');
            // Highlight selected star and all previous stars
            for (let i = 0; i <= index; i++) {
                stars[i].style.color = '#FFD700';
            }
        });
    });
    
    playbackBar.addEventListener('input', () => {
        console.log("input event activated")
        const totalSeconds = parseInt(playbackBar.value, 10);
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        currentTimeDisplay.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        console.log(currentTimeDisplay.textContent)
        document.getElementById('comment-timestamp').value = playbackBar.value;
    });

    playbackBar.addEventListener('mouseup', () =>{
        console.log("mouse_up event triggered")
        fetch(`/comments?media_id=${id}&timestamp=${playbackBar.value}&media_type=movie`)
        .then(response => response.json())
        .then(data => {
            commentsList.innerHTML = '';
            data.forEach(comment => {
                const commentElement = document.createElement('li');
                commentElement.textContent = `${comment.username}: ${comment.text}`;
                commentsList.appendChild(commentElement);
            });
        });
    })

    commentForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const formData = new FormData(commentForm);

        fetch(commentForm.action, {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.redirected) {
                window.location.href = response.url;
            }
        });
    });


});
