// Navigation Component Loader
document.addEventListener('DOMContentLoaded', function() {
    // Check if Alpine.js is loaded
    if (typeof Alpine === 'undefined') {
        const alpineScript = document.createElement('script');
        alpineScript.src = 'https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js';
        alpineScript.defer = true;
        document.head.appendChild(alpineScript);
    }
    
    // Load navigation component
    loadNavigation();
});

function loadNavigation() {
    const navContainer = document.getElementById('navigation-container');
    if (!navContainer) {
        console.error('Navigation container not found');
        return;
    }

    fetch('../components/navigation.html')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            navContainer.innerHTML = html;
            // Initialize Alpine.js after loading
            setTimeout(() => {
                if (typeof Alpine !== 'undefined' && Alpine.start) {
                    Alpine.start();
                }
                setActiveNavLink();
            }, 100);
        })
        .catch(error => {
            console.error('Navigation failed to load:', error);
            navContainer.innerHTML = '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">Navigation failed to load</div>';
        });
}

// Set active navigation link based on current page
function setActiveNavLink() {
    const currentPage = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('.nav-link, .mobile-nav-link');
    
    navLinks.forEach(link => {
        const linkPage = link.getAttribute('href');
        if (linkPage === currentPage) {
            link.classList.add('active');
        }
    });
}