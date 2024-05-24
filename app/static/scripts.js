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
    const featureContainer = document.querySelector('.feature-container');
    const featureBoxes = document.querySelectorAll('.feature-box');
    const controls = useAnimation();

    let currentIndex = 0;

    const scrollHandler = (e) => {
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
        controls.start({
            y: -currentIndex * window.innerHeight,
            transition: { duration: 0.5, ease: 'easeOut' }
        });
    };

    // Apply Framer Motion animations
    featureBoxes.forEach((featureBox, index) => {
        motion(featureBox, {
            initial: { opacity: 0, y: 50 },
            animate: { opacity: 1, y: 0 },
            transition: { duration: 0.5, delay: index * 0.2, ease: 'easeOut' }
        });
    });

    // Initial animation setup
    animateFeatures();

    // Event listener for scroll
    window.addEventListener('wheel', scrollHandler, { passive: false });
});
