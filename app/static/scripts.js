import { motion, animate } from "framer-motion";

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
    const features = document.querySelectorAll('.feature-box');
    features.forEach(feature => {
        animate(feature, { opacity: 1, y: 0 }, { duration: 0.5, ease: "easeOut" });
    });
});
