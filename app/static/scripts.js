// scripts.js
// Add any custom JavaScript for interactivity

document.addEventListener('DOMContentLoaded', function() {
    const typingEffect = document.getElementById('typing-effect');
    if (typingEffect) {
        const text = typingEffect.textContent;
        typingEffect.textContent = '';
        let index = 0;

        function typeEffect() {
            if (index < text.length) {
                typingEffect.textContent += text.charAt(index);
                index++;
                setTimeout(typeEffect, 100);
            }
        }

        typeEffect();
    }

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
});
