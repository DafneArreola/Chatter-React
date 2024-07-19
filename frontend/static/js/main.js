document.addEventListener('DOMContentLoaded', function () {
    fetchMovies();
});

function fetchMovies() {
    fetch('/movies')
        .then(response => response.json())
        .then(data => {
            const movieList = document.getElementById('movie-list');
            movieList.innerHTML = data.map(movie => `
                <div class="col-md-4 mb-4">
                    <div class="card">
                        <img src="https://image.tmdb.org/t/p/w500/${movie.poster_path}" class="card-img-top" alt="${movie.title}">
                        <div class="card-body">
                            <h5 class="card-title">${movie.title}</h5>
                            <a href="/movie/${movie.id}" class="btn btn-primary">View Details</a>
                        </div>
                    </div>
                </div>
            `).join('');
        });
}
