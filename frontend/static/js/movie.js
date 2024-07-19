document.addEventListener('DOMContentLoaded', function () {
    const movieId = window.location.pathname.split('/').pop();
    fetchMovieDetails(movieId);
    setupRatingForm(movieId);
    setupCommentForm(movieId);
    setupTimestampScroll(movieId);
});

function fetchMovieDetails(movieId) {
    fetch(`/movie/${movieId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('movie-title').textContent = data.title;
            document.getElementById('movie-poster').src = `https://image.tmdb.org/t/p/w500/${data.poster_path}`;
            document.getElementById('movie-overview').textContent = data.overview;
        });
}

function setupRatingForm(movieId) {
    document.getElementById('rating-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const rating = document.getElementById('rating').value;
        fetch('/rate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: 1,  // Replace with actual user ID
                media_id: movieId,
                rating: rating
            })
        }).then(response => response.json())
          .then(data => {
              alert(data.message);
          });
    });
}

function setupCommentForm(movieId) {
    document.getElementById('comment-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const timestamp = document.getElementById('timestamp').value;
        const content = document.getElementById('comment').value;
        fetch('/comment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: 1,  // Replace with actual user ID
                media_id: movieId,
                timestamp: timestamp,
                content: content
            })
        }).then(response => response.json())
          .then(data => {
              alert(data.message);
              fetchComments(movieId, timestamp);
          });
    });
}

function setupTimestampScroll(movieId) {
    const timestampRange = document.getElementById('timestamp-range');
    const timestampLabel = document.getElementById('timestamp-label');
    
    timestampRange.addEventListener('input', function () {
        timestampLabel.textContent = this.value;
        fetchComments(movieId, this.value);
    });
}

function fetchComments(movieId, timestamp) {
    fetch(`/comments/${movieId}/${timestamp}`)
        .then(response => response.json())
        .then(data => {
            const commentList = document.getElementById('comment-list');
            commentList.innerHTML = data.map(comment => `
                <div class="comment">
                    <p><strong>User ${comment.user_id}</strong>: ${comment.content}</p>
                    <p class="text-muted">${new Date(comment.created_at).toLocaleString()}</p>
                </div>
            `).join('');
        });
}
