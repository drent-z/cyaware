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

    // Framer Motion scroll animation
    const featureBoxes = document.querySelectorAll('.feature-box');
    const controls = useAnimation();

    // Function to check if element is in viewport
    const isInViewport = (element) => {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    };

    // Apply Framer Motion animations
    featureBoxes.forEach((featureBox, index) => {
        motion(featureBox, {
            initial: { opacity: 0, y: 50 },
            animate: { opacity: 1, y: 0 },
            transition: { duration: 0.5, delay: index * 0.2, ease: 'easeOut' }
        });
    });

    // Scroll event listener to animate feature boxes when they come into view
    window.addEventListener('scroll', () => {
        featureBoxes.forEach((featureBox, index) => {
            if (isInViewport(featureBox)) {
                controls.start({
                    opacity: 1,
                    y: 0,
                    transition: { duration: 0.5, delay: index * 0.2, ease: 'easeOut' }
                });
            }
        });
    });

    // Initial check for elements in the viewport
    featureBoxes.forEach((featureBox) => {
        if (isInViewport(featureBox)) {
            controls.start({
                opacity: 1,
                y: 0,
                transition: { duration: 0.5, ease: 'easeOut' }
            });
        }
    });
});
