$(document).ready(function() {

    const progressBar = document.getElementById('progressBar');
    let width = 0;

    function updateProgressBar() {
        $.getJSON('/get_live_player_info', function(data) {
            // if nothign is playing 

            if (data.length === 0) {
                console.log("nothing playing")
                return
            
            // if somethign is there
            } else if (data.length > 1) {
                //playback_status = currently_playing_response.json()
        
                progress_ms = playback_status.progress_ms
                duration_ms = playback_status.item.duration_ms

                let currentProgress = progress_ms;
                let duration = duration_ms;
                let progress = (currentProgress / duration) * 100;
                
                $('#progressBar').css('width', progress + '%');

            // if error occurs
            } else {
                console.log('an error occured somewhere')
                return
            }




        });
    }

    setInterval(updateProgressBar, 1000)
});