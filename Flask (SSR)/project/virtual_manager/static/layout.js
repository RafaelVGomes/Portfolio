document.addEventListener('DOMContentLoaded', function() {
    // Compares if the 3rd part of the visited and <li> href link matches
    document.querySelectorAll(".nav-link").forEach((x) => {
        if (window.location.href.split('/')[3] == x.href.split('/')[3]) {
            x.classList.add('active', 'disabled')
        }
    })
})
