document.addEventListener('DOMContentLoaded', (event) => {
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
