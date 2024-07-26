$(document).ready(function() {
    const playbackBar = document.getElementById('playback-bar');
    const img = document.getElementById("player-image");
    const name = document.getElementById("player-name");
    const timestamp = document.getElementById("timestamp");
    const playPauseButton = document.getElementById("play-pause")
    const commentsList = document.getElementById('comments-list');

    // Track playback state
    let is_playing = false;
    let media_id = "";
    let timestamp_value = 0;
    let device_id = "";

    function create_time_string(time) {
        let seconds = (Math.floor(time / 1000)) % 60;
        let total_duration_seconds = Math.floor(time / 1000);
        let minutes = Math.floor(total_duration_seconds / 60);

        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    function updateProgressBar() {
        $.getJSON('/get_live_player_info', function(data) {
            if (Object.keys(data).length === 0) {
                device_id = "";
                media_id = "";
                img.src = "";
                name.innerText = "No Song Playing";
                timestamp_value = 0;
                timestamp.innerText = "0:00 / 0:00";
                playbackBar.value = 0;
                playbackBar.max = 100; // Set to some default value
            } else {
                device_id = data.device.id;
                let progress_ms = data.progress_ms;
                let duration_ms = data.item.duration_ms;
                let progress_str = create_time_string(progress_ms) + " / " + create_time_string(duration_ms);
                let progress_seconds = Math.floor(progress_ms / 1000);
                
                playbackBar.value = progress_seconds;
                playbackBar.max = Math.floor(duration_ms / 1000);
                timestamp_value = progress_ms;
                timestamp.innerText = progress_str;

                is_playing = data.is_playing;
                playPauseButton.innerText = is_playing ? "Pause" : "Play";

                if (img.src !== data.item.album.images[1].url) {
                    img.src = data.item.album.images[1].url;
                    media_id = data.item.id;
                    name.innerText = data.item.name;
                }
            }
        });
    }

    document.getElementById("play-pause").addEventListener("click", () => {
        if (device_id === "") {
            console.log("Nothing playing");
        } else {
            const action = is_playing ? `/pause_player?device_id=${device_id}` : `/play_player?device_id=${device_id}`;
            $.getJSON(action, (data) => {
                console.log(data);
            });
        }
    });

    function updateComments() {
        if (media_id !== "") {
            $.getJSON(`/spotify_player_obtain_comments?media_id=${media_id}&timestamp=${Math.floor(timestamp_value / 1000)}`, function(data) {
                commentsList.innerHTML = '';
                data.forEach(comment => {
                    const commentElement = document.createElement('li');
                    commentElement.textContent = `${comment.username}: ${comment.text} - ${comment.timestamp}`;
                    commentsList.appendChild(commentElement);
                });
            });
        }
    }

    setInterval(updateProgressBar, 1000);
    setInterval(updateComments, 3000);
});
