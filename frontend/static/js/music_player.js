$(document).ready(function() {
    // // Progress Bar that goes up every second
    
    // const progressBar = document.getElementById('progressBar');
    // let width = 0;
    // const interval = setInterval(() => {
    //     if (width >= 100) {
    //         clearInterval(interval);
    //     } else {
    //         width++;
    //         progressBar.style.width = `${width}%`;
    //         progressBar.setAttribute('aria-valuenow', width);
    //         console.log(`this john works`);
    //     }
    
    // progress bar that makes call to api once every second
    
    const progressBar = document.getElementById('progressBar');
    let width = 0;

    function updateProgressBar() {
        $.getJSON('/control_playback', function(data) {
            let currentProgress = data.progress_ms;
            let duration = data.duration_ms;
            let progress = (currentProgress / duration) * 100;
            
            $('#progressBar').css('width', progress + '%');

        });
    }

    setInterval(updateProgressBar, 1000)
});