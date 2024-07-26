$(document).ready(function() {

    const progressBar = document.getElementById('progressBar');
    let width = 0;

    const img = document.getElementById("player-image");
    const name = document.getElementById("player-name");
    const timestamp = document.getElementById("timestamp");
    const playPauseButton = document.getElementById("play-pause")

    // this is the variable we use to keep track of if song switches
    let current_image = img.src
    let is_playing = false;
    let media_id = "";
    let timestamp_value = 0;

    // this is the variable we will use to pause and play
    // if it is empty, do not allow pause or play to make a call to route
    let device_id = "";

    function create_time_string(time) {
        
        let seconds = (Math.floor(time / 1000)) % 60 

        let total_duration_seconds = Math.floor(time / 1000) 
        let minutes = Math.floor(total_duration_seconds / 60)

        if (minutes < 10){
            minutes = '0' + minutes.toString()
        } else {
            minutes =  minutes.toString()
        }

        if (seconds < 10){
            seconds = '0' + seconds.toString()
        } else {
            seconds = seconds.toString()
        }

        return `${minutes}:${seconds}`
    }
    

    function updateProgressBar() {
        $.getJSON('/get_live_player_info', function(data) {
            let len = count = Object.keys(data).length;

            // handles if nothing is playing
            if (len === 0) {
                device_id = ""
                media_id = ""
                img.src = ""
                name.innerText = ""
                timestamp_value=0
                timestamp.innerText = ""
                console.log("nothing playing")
            
            // handles if something is there
            } else if (len > 1) {
                // calculate progress and duration, and update propgress bar and timestamp
                // updates user_id
                device_id = data.device.id

                let progress_ms = data.progress_ms
                let duration_ms = data.item.duration_ms
                let progress_str = create_time_string(progress_ms) + " / " + create_time_string(duration_ms);
                let progress_percentage = (progress_ms / duration_ms) * 100;
                
                console.log('mde it to progress')
                $('#progressBar').css('width', progress_percentage + '%');
                timestamp_value = progress_ms
                timestamp.innerText = progress_str
                

                // update progress id
                is_playing = data.is_playing
                console.log(`is_playing`)
                if (is_playing) {
                    playPauseButton.innerText = "pause"
                } else {
                    playPauseButton.innerText = "play"
                }

                // update the page if the song changes
                if (img != data.item.album.images[1].url) {
                    img.src = data.item.album.images[1].url
                    current_image = img.src
                    media_id = data.item.id
                    name.innerText = data.item.name
                    timestamp.inner_text = progress_str
                    timestamp_value = progress_ms
                }

            // handles if error occurs
            } else {
                console.log('an error occured somewhere')
            }
        });


    }

    document.getElementById("play-pause").addEventListener("click", ()=> {
        // handle if there is nothing playing
        if (device_id === "") {
            console.log("nothing playing")

        // handle if there is someting playing
        } else {
            if (is_playing){
                $.getJSON(`/pause_player?device_id=${device_id}`, (data) => {
                    console.log(data)
                })
            } else if (!is_playing) {
                $.getJSON(`/play_player?device_id=${device_id}`, (data) => {
                    console.log(data)
                })
            } else {
                console.log('trying to pause or play, but is_playing attribute is not a boolean')
            }

        }

    })

    
    function updateComments() {
        $.getJSON(`/spotify_player_obtain_comments?media_id=${media_id}&timestamp=${timestamp_value}`, function(data) {
            let len = count = Object.keys(data).length;console.log()

        });
    }



    setInterval(updateProgressBar, 1000)
    setInterval(updateComments, 3000)
});