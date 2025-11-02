/**
 * Admin Navigation JavaScript
 * Based on sample navigation structure for consistent functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin navigation initializing...');
    
    // Initialize mobile menu functionality
    initializeMobileMenu();
    
    // Initialize dropdown menus
    initializeDropdowns();
    
    // Set active page in navigation
    setActivePage();
    
    // Initialize search functionality
    initializeSearch();
    
    console.log('Admin navigation initialized successfully');
});

/**
 * Initialize mobile menu toggle functionality
 */
function initializeMobileMenu() {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    
    if (menuToggle && sidebar) {
        // Toggle sidebar on menu button click
        menuToggle.addEventListener('click', function() {
            console.log('Mobile menu toggle clicked');
            sidebar.classList.toggle('-translate-x-full');
            
            if (overlay) {
                overlay.classList.toggle('hidden');
            }
        });
        
        // Close sidebar when clicking overlay
        if (overlay) {
            overlay.addEventListener('click', function() {
                console.log('Overlay clicked, closing sidebar');
                sidebar.classList.add('-translate-x-full');
                overlay.classList.add('hidden');
            });
        }
        
        // Handle window resize
        window.addEventListener('resize', function() {
            if (window.innerWidth >= 1024) { // lg breakpoint
                sidebar.classList.remove('-translate-x-full');
                if (overlay) {
                    overlay.classList.add('hidden');
                }
            }
        });
        
        console.log('Mobile menu initialized');
    } else {
        console.warn('Mobile menu elements not found');
    }
}

/**
 * Initialize dropdown functionality for notifications and profile
 */
function initializeDropdowns() {
    // Notifications dropdown
    const notificationsToggle = document.getElementById('notifications-toggle');
    const notificationsDropdown = document.getElementById('notifications-dropdown');
    
    if (notificationsToggle && notificationsDropdown) {
        notificationsToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            notificationsDropdown.classList.toggle('hidden');
            
            // Close profile dropdown if open
            const profileDropdown = document.getElementById('profile-dropdown');
            if (profileDropdown) {
                profileDropdown.classList.add('hidden');
            }
        });
        console.log('Notifications dropdown initialized');
    }
    
    // Profile dropdown
    const profileToggle = document.getElementById('profile-toggle');
    const profileDropdown = document.getElementById('profile-dropdown');
    
    if (profileToggle && profileDropdown) {
        profileToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            profileDropdown.classList.toggle('hidden');
            
            // Close notifications dropdown if open
            if (notificationsDropdown) {
                notificationsDropdown.classList.add('hidden');
            }
        });
        console.log('Profile dropdown initialized');
    }
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (notificationsDropdown && !notificationsDropdown.contains(e.target)) {
            notificationsDropdown.classList.add('hidden');
        }
        if (profileDropdown && !profileDropdown.contains(e.target)) {
            profileDropdown.classList.add('hidden');
        }
    });
    
    console.log('Dropdowns initialized');
}

/**
 * Set active page in navigation based on current URL
 */
function setActivePage() {
    const currentPage = window.location.pathname.split('/').pop().replace('.html', '') || 'dashboard';
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href) {
            const linkPage = href.split('/').pop().replace('.html', '');
            
            if (linkPage === currentPage) {
                // Remove existing active classes
                navLinks.forEach(l => {
                    l.classList.remove('bg-primary-100', 'text-primary-700', 'border-primary-500');
                    l.classList.add('text-gray-900');
                });
                
                // Add active classes to current link
                link.classList.remove('text-gray-900');
                link.classList.add('bg-primary-100', 'text-primary-700');
                
                // Update icon color for active link
                const icon = link.querySelector('i');
                if (icon) {
                    icon.classList.remove('text-primary-500');
                    icon.classList.add('text-primary-700');
                }
                
                console.log('Active page set to:', currentPage);
            }
        }
    });
}

/**
 * Initialize search functionality
 */
function initializeSearch() {
    const searchInput = document.querySelector('input[type="search"]');
    
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const query = this.value.trim();
                if (query) {
                    console.log('Search query:', query);
                    // Here you would typically redirect to a search results page
                    // window.location.href = `search.html?q=${encodeURIComponent(query)}`;
                }
            }
        });
        
        console.log('Search functionality initialized');
    }
}

/**
 * Utility function to show notifications (can be called from other scripts)
 */
function showNotification(message, type = 'info') {
    console.log(`Notification [${type}]: ${message}`);
    
    // Update notification badge
    const badge = document.getElementById('notification-badge');
    if (badge) {
        const currentCount = parseInt(badge.textContent) || 0;
        badge.textContent = currentCount + 1;
        badge.classList.remove('hidden');
    }
    
    // Here you could add toast notifications or update the dropdown content
}

/**
 * Utility function to update badge counts
 */
function updateBadgeCounts() {
    // Example: Update pending residents badge
    const pendingBadge = document.getElementById('pending-residents-badge');
    if (pendingBadge) {
        // This would typically come from an API call
        // For now, we'll just use a placeholder
        console.log('Badge counts updated');
    }
    
    // Example: Update certificate requests badge
    const certBadge = document.getElementById('certificate-requests-badge');
    if (certBadge) {
        // This would typically come from an API call
        console.log('Certificate badge updated');
    }
}

// Call badge update on load
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(updateBadgeCounts, 1000); // Delay to ensure DOM is fully loaded
});

// Export functions for use in other scripts
window.AdminNavigation = {
    showNotification,
    updateBadgeCounts,
    setActivePage
};