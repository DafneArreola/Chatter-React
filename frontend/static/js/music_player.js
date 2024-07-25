$(document).ready(function() {

    const progressBar = document.getElementById('progressBar');
    let width = 0;
    const img = document.getElementById("player-image");
    current_image = img.src
    

    function updateProgressBar() {
        $.getJSON('/get_live_player_info', function(data) {

            let len = count = Object.keys(data).length;
            device_id = img.device.id

            console.log(len)


            if (len === 0) {
                console.log("nothing playing")
                return
            
            // if somethign is there
            } else if (len > 1) {
                //playback_status = currently_playing_response.json()
                // if nothign is playing 

                if (img != data.item.album.images[1].url) {
                    img.src = data.item.album.images[1].url
                    current_image = img.src

                    let name = document.getElementById("player-name") 
                    name.innerText = data.item.name

                }
        

                progress_ms = data.progress_ms
                duration_ms = data.item.duration_ms

                let currentProgress = progress_ms;
                let duration = duration_ms;
                let progress = (currentProgress / duration) * 100;
                
                $('#progressBar').css('width', progress + '%');

                
        
               return

            // if error occurs
            } else {
                console.log('an error occured somewhere')
                return
            }



        });
    }

    setInterval(updateProgressBar, 1000)
});