// Import Framer Motion functions
import { motion } from 'framer-motion';

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', (event) => {
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

    // Function to detect if the device is mobile
    const isMobile = () => window.innerWidth <= 992;

    // Scroll hijacking
    const featureContainer = document.querySelector('.feature-container');
    const featureBoxes = document.querySelectorAll('.feature-box');

    let currentIndex = 0;

    const scrollHandler = (e) => {
        if (!isMobile()) return;

        e.preventDefault();

        if (e.deltaY > 0) {
            if (currentIndex < featureBoxes.length - 1) {
                currentIndex++;
            }
        } else {
            if (currentIndex > 0) {
                currentIndex--;
            }
        }

        animateFeatures();
    };

    const animateFeatures = () => {
        featureBoxes.forEach((box, index) => {
            if (index < currentIndex) {
                box.style.transform = `translateY(-100%)`;
            } else if (index === currentIndex) {
                box.style.transform = `translateY(0)`;
            } else {
                box.style.transform = `translateY(100%)`;
            }
        });
    };

    // Initial animation setup
    animateFeatures();

    // Event listener for scroll
    window.addEventListener('wheel', scrollHandler, { passive: false });
    window.addEventListener('touchmove', scrollHandler, { passive: false });
});
