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

    // Toggle Navbar
    const navbarToggle = document.getElementById('navbar-toggle');
    const navLinks = document.getElementById('nav-links');

    navbarToggle.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        navLinks.classList.add('animate__animated', 'animate__fadeInDown');
        setTimeout(() => {
            navLinks.classList.remove('animate__animated', 'animate__fadeInDown');
        }, 1000);
    });
});
