document.addEventListener('DOMContentLoaded', function() {
    // Compares if the 3rd part of the visited link and <li> href link matches
    const url_prefix = $('#index-tabs').length ? 3 : 4
    const layoutNavbar = document.getElementById('layoutNavbar')
    layoutNavbar.querySelectorAll(".nav-link").forEach((x) => {
      if (window.location.href.split('/')[url_prefix] == x.href.split('/')[url_prefix]) {
        x.classList.add('active', 'disabled')
      }
    })
})
