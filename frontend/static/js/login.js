document.addEventListener("DOMContentLoaded", function() {
    const blob = document.querySelector('.blob');
    const duration = 10; // Animation duration in seconds
    let currentPosition = { x: window.innerWidth / 2, y: window.innerHeight / 2 }; // Initial position at the center

    // Create a <style> element
    const styleElement = document.createElement('style');
    document.head.appendChild(styleElement);

    function getRandomPosition() {
        const screenWidth = window.innerWidth;
        const screenHeight = window.innerHeight;
        const maxX = screenWidth - blob.clientWidth;
        const maxY = screenHeight - blob.clientHeight;

        const randomX = Math.floor(Math.random() * maxX);
        const randomY = Math.floor(Math.random() * maxY);

        return { x: randomX, y: randomY };
    }

    function updateAnimation() {
        const keyframes = [];
        const startPosition = currentPosition;
        
        for (let i = 25; i <= 100; i += 25) {
            const { x, y } = getRandomPosition();
            keyframes.push(`${i}% { transform: translate(${x}px, ${y}px); }`);
            if (i === 100) {
                currentPosition = { x, y }; // Update the current position at the end of the cycle
            }
        }

        const animationName = 'move';
        styleElement.innerHTML = `@keyframes ${animationName} {
            0% { transform: translate(${startPosition.x}px, ${startPosition.y}px); }
            ${keyframes.join(' ')}
        }`;

        // Reset the animation to ensure smooth transition
        blob.style.animation = 'none';
        // Force reflow
        blob.offsetHeight;
        blob.style.animation = `move ${duration}s linear infinite`;

        console.log(`Updated keyframes: @keyframes ${animationName} {
            0% { transform: translate(${startPosition.x}px, ${startPosition.y}px); }
            ${keyframes.join(' ')}
        }`); // Debug log
    }

    updateAnimation();
    setInterval(updateAnimation, duration * 1000);
});