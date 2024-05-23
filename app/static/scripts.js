// scripts.js
// Add any custom JavaScript for interactivity

document.addEventListener('DOMContentLoaded', function() {
    const floatingWidget = document.querySelector('.floating-widget');
    const closeBtn = document.createElement('span');
    closeBtn.textContent = '✖';
    closeBtn.style.position = 'absolute';
    closeBtn.style.top = '10px';
    closeBtn.style.right = '10px';
    closeBtn.style.cursor = 'pointer';
    closeBtn.style.color = '#ff0000';
    floatingWidget.appendChild(closeBtn);
    closeBtn.addEventListener('click', () => {
        floatingWidget.style.display = 'none';
    });

    // Add a cool typing effect to the welcome message
    const welcomeMessage = document.querySelector('.floating-widget h3');
    const welcomeText = welcomeMessage.textContent;
    welcomeMessage.textContent = '';
    let index = 0;

    function typeEffect() {
        if (index < welcomeText.length) {
            welcomeMessage.textContent += welcomeText.charAt(index);
            index++;
            setTimeout(typeEffect, 100);
        }
    }

    typeEffect();
});
