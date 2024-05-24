// Ensure you include Framer Motion
import { motion } from "framer-motion";

// Auto fade out flash messages after 3 seconds
setTimeout(() => {
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach((msg) => {
        msg.classList.add('animate__fadeOutUp');
        setTimeout(() => {
            msg.remove();
        }, 1000); // Ensure the fade-out animation completes before removing
    });
}, 3000);

// Close button functionality
document.querySelectorAll('.alert .close').forEach((button) => {
    button.addEventListener('click', (event) => {
        const alert = event.target.closest('.alert');
        alert.classList.add('animate__fadeOutUp');
        setTimeout(() => {
            alert.remove();
        }, 1000); // Ensure the fade-out animation completes before removing
    });
});

// Navbar toggle functionality using jQuery
$('.navbar-toggler').click(function() {
    $('.navbar-collapse').toggleClass('show');
});

// Add Framer Motion animations
const hero = document.querySelector('.hero');
const features = document.querySelectorAll('.feature-box');

// Create a function to add motion elements
function addMotion(element) {
    const motionElement = motion(element);
    motionElement.setAttribute('initial', { opacity: 0, y: 50 });
    motionElement.setAttribute('animate', { opacity: 1, y: 0 });
    motionElement.setAttribute('transition', { duration: 0.5, ease: "easeOut" });
    return motionElement;
}

// Apply the motion elements
addMotion(hero);
features.forEach(feature => addMotion(feature));
