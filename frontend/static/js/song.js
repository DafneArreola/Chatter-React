// frontend/static/js/song.js

document.addEventListener('DOMContentLoaded', () => {
    const playbackBar = document.querySelector('.playback-bar input[type="range"]'); 
    const currentTimeDisplay = document.getElementById('current-time');
    const totalTimeDisplay = document.getElementById('total-time');
    const commentForm = document.getElementById('comment-form');
    const commentsList = document.getElementById('comments-list');

    const stars = document.querySelectorAll('.stars label');
    const userRating = window.userRating;

    stars.forEach((star, index) => {
        star.addEventListener('click', () => {
            // Clear all stars
            stars.forEach(s => s.querySelector('.fa-star').style.color = '#ccc');
            // Highlight selected star and all previous stars
            for (let i = 0; i <= index; i++) {
                stars[i].querySelector('.fa-star').style.color = '#FFD700';
            }
        });
    });

    // Highlight stars based on user rating
    if (userRating > 0) {
        stars.forEach((star, index) => {
            if (index < userRating) {
                star.querySelector('.fa-star').style.color = '#FFD700';
            }
        });
    }

    playbackBar.addEventListener('input', () => {
        const totalSeconds = parseInt(playbackBar.value, 10);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        currentTimeDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        //console.log(currentTimeDisplay.textContent)
        document.getElementById('comment-timestamp').value = playbackBar.value;
        console.log('func works')
    });

    playbackBar.addEventListener('mouseup', () =>{
        console.log('Mouse up event triggered');
        console.log(playbackBar.value)
        fetch(`/comments?media_id=${id}&timestamp=${playbackBar.value}&media_type=song`)
        .then(response => response.json())
        .then(data => {
            commentsList.innerHTML = '';
            data.forEach(comment => {
                const commentElement = document.createElement('li');
        
                // Create a link for the username
                const usernameLink = document.createElement('a');
                usernameLink.href = `/user/${comment.user_id}`;  // Link to the user's profile page
                usernameLink.textContent = comment.username;
                usernameLink.style.color = '#007bff'; // Optional: style link
                usernameLink.style.textDecoration = 'none'; // Optional: remove underline

                // Append username link and comment text
                commentElement.appendChild(usernameLink);
                commentElement.appendChild(document.createTextNode(`: ${comment.text}`));
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

