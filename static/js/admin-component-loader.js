// Admin Component Loader for Dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin component loader starting...');
    loadAdminComponents();
});

function loadAdminComponents() {
    console.log('Loading admin components...');
    // Load sidebar first, then header
    loadAdminSidebar();
    loadAdminHeader();
}

function loadAdminSidebar() {
    console.log('Loading admin sidebar...');
    const sidebarContainer = document.getElementById('admin-sidebar');
    if (!sidebarContainer) {
        console.error('Admin sidebar container not found');
        return;
    }

    console.log('Sidebar container found, fetching component...');
    fetch('../components/admin-sidebar.html')
        .then(response => {
            console.log('Sidebar fetch response:', response.status, response.statusText);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            console.log('Sidebar HTML loaded, length:', html.length);
            sidebarContainer.innerHTML = html;
            console.log('Sidebar HTML injected into container');
            
            // Initialize sidebar functionality after loading
            initializeSidebarFunctionality();
        })
        .catch(error => {
            console.error('Error loading admin sidebar:', error);
            sidebarContainer.innerHTML = '<div class="p-4 text-red-600">Error loading sidebar</div>';
        });
}

function loadAdminHeader() {
    console.log('Loading admin header...');
    const headerContainer = document.getElementById('admin-header');
    if (!headerContainer) {
        console.error('Admin header container not found');
        return;
    }

    console.log('Header container found, fetching component...');
    fetch('../components/admin-header.html')
        .then(response => {
            console.log('Header fetch response:', response.status, response.statusText);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            console.log('Header HTML loaded, length:', html.length);
            headerContainer.innerHTML = html;
            console.log('Header HTML injected into container');
            
            // Initialize header functionality after loading
            initializeHeaderFunctionality();
        })
        .catch(error => {
            console.error('Error loading admin header:', error);
            headerContainer.innerHTML = '<div class="p-4 text-red-600">Error loading header</div>';
        });
}

function initializeSidebarFunctionality() {
    console.log('Initializing sidebar functionality...');
    
    // Load and initialize the admin navigation JavaScript
    if (!document.querySelector('script[src*="admin-navigation.js"]')) {
        const script = document.createElement('script');
        script.src = '../assets/js/admin-navigation.js';
        script.onload = function() {
            console.log('Admin navigation script loaded');
        };
        script.onerror = function() {
            console.error('Failed to load admin navigation script');
        };
        document.head.appendChild(script);
    }
    
    // Add Font Awesome for icons if not already loaded
    if (!document.querySelector('link[href*="font-awesome"]')) {
        const fontAwesome = document.createElement('link');
        fontAwesome.rel = 'stylesheet';
        fontAwesome.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
        document.head.appendChild(fontAwesome);
        console.log('Font Awesome loaded');
    }
}

function initializeHeaderFunctionality() {
    console.log('Initializing header functionality...');
    
    // The admin-navigation.js script handles header functionality as well
    // No additional initialization needed here
}