document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('navbar-toggle');
    const navLinks = document.getElementById('nav-links');

    toggleButton.addEventListener('click', function () {
        navLinks.classList.toggle('active');
        toggleButton.classList.toggle('open');
    });
});
