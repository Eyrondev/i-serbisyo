// Component Loader for Admin Dashboard
class ComponentLoader {
    static async loadComponent(componentPath, targetSelector) {
        try {
            const response = await fetch(componentPath);
            if (!response.ok) {
                throw new Error(`Failed to load component: ${response.status}`);
            }
            const componentHTML = await response.text();
            const targetElement = document.querySelector(targetSelector);
            if (targetElement) {
                targetElement.innerHTML = componentHTML;
                console.log(`Loaded component: ${componentPath}`);
            }
        } catch (error) {
            console.error('Error loading component:', error);
        }
    }
    
    static async loadComponents() {
        // Load admin sidebar
        await this.loadComponent('../components/admin-sidebar.html', '#admin-sidebar');
        
        // Load admin header  
        await this.loadComponent('../components/admin-header.html', '#admin-header');
        
        console.log('All components loaded successfully');
    }
}

// Initialize components when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Wait a bit for Alpine.js to initialize first
    setTimeout(() => {
        ComponentLoader.loadComponents();
    }, 100);
});

// Also try to load when Alpine is ready
document.addEventListener('alpine:init', function() {
    console.log('Alpine.js initialized');
});