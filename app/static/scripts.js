// Import Framer Motion functions
import { motion, useAnimation } from 'framer-motion';

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

    // Apply Framer Motion animations
    const heroSection = document.getElementById('hero-section');
    const featuresSection = document.getElementById('features-section');
    const featureBoxes = document.querySelectorAll('.feature-box');

    // Animate Hero Section
    if (heroSection) {
        motion(heroSection, {
            initial: { opacity: 0, y: -50 },
            animate: { opacity: 1, y: 0 },
            transition: { duration: 1, ease: 'easeOut' }
        });
    }

    // Animate Features Section
    if (featuresSection) {
        motion(featuresSection, {
            initial: { opacity: 0 },
            animate: { opacity: 1 },
            transition: { duration: 1.5, ease: 'easeOut' }
        });
    }

    // Animate Feature Boxes
    featureBoxes.forEach((featureBox, index) => {
        motion(featureBox, {
            initial: { opacity: 0, y: 50 },
            animate: { opacity: 1, y: 0 },
            transition: { duration: 0.5, delay: index * 0.2, ease: 'easeOut' }
        });
    });
});
