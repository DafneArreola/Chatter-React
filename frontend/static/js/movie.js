document.addEventListener('DOMContentLoaded', () => {
    const playbackBar = document.querySelector('.playback-bar input[type="range"]');
    const currentTimeDisplay = document.getElementById('current-time');
    const totalTimeDisplay = document.getElementById('total-time');

    playbackBar.addEventListener('input', () => {
        const totalSeconds = parseInt(playbackBar.value, 10);
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        currentTimeDisplay.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    });

    // Initialize total time
    const totalRuntimeSeconds = parseInt(playbackBar.max, 10);
    const totalHours = Math.floor(totalRuntimeSeconds / 3600);
    const totalMinutes = Math.floor((totalRuntimeSeconds % 3600) / 60);
    const totalSeconds = totalRuntimeSeconds % 60;

    totalTimeDisplay.textContent = `${totalHours.toString().padStart(2, '0')}:${totalMinutes.toString().padStart(2, '0')}:${totalSeconds.toString().padStart(2, '0')}`;

    const stars = document.querySelectorAll('.stars label');
    let currentRating = 0;

    stars.forEach((star, index) => {
        star.addEventListener('mouseover', () => {
            stars.forEach((s, i) => {
                s.style.color = i <= index ? 'gold' : '#ccc';
            });
        });

        star.addEventListener('mouseout', () => {
            stars.forEach((s, i) => {
                s.style.color = i < currentRating ? 'gold' : '#ccc';
            });
        });

        star.addEventListener('click', () => {
            currentRating = index + 1;
            document.querySelector(`input[name="rating"][value="${currentRating}"]`).checked = true;
            stars.forEach((s, i) => {
                s.style.color = i < currentRating ? 'gold' : '#ccc';
            });
        });
    });

});
