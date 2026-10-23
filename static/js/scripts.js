// static/js/scripts.js

// Navigation scroll behavior
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');

    if (!mainNav) return; // Guard clause if nav doesn't exist

    const headerHeight = mainNav.clientHeight;

    window.addEventListener('scroll', () => {
        const currentTop = document.body.getBoundingClientRect().top * -1;

        if (currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove('is-visible');
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }

        scrollPos = currentTop;
    });
});