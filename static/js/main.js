/**
 * Modern i-Serbisyo Frontend JavaScript
 * Author: i-Serbisyo Development Team
 * Description: Modern interactive components and utilities
 */

// Main Application Object
const iSerbisyo = {
  // Initialize application
  init() {
    this.setupEventListeners();
    this.initializeComponents();
    this.setupScrollEffects();
    this.setupFormValidation();
    console.log('🚀 i-Serbisyo Frontend Initialized');
  },

  // Event Listeners
  setupEventListeners() {
    // Mobile menu toggle
    this.setupMobileMenu();
    
    // Smooth scrolling for anchor links
    this.setupSmoothScrolling();
    
    // Modal controls
    this.setupModals();
    
    // Dropdown menus
    this.setupDropdowns();
    
    // Search functionality
    this.setupSearch();
  },

  // Mobile Menu Implementation
  setupMobileMenu() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
      mobileMenuButton.addEventListener('click', () => {
        const isHidden = mobileMenu.classList.contains('hidden');
        
        if (isHidden) {
          mobileMenu.classList.remove('hidden');
          mobileMenu.classList.add('animate-slide-down');
          mobileMenuButton.setAttribute('aria-expanded', 'true');
        } else {
          mobileMenu.classList.add('hidden');
          mobileMenu.classList.remove('animate-slide-down');
          mobileMenuButton.setAttribute('aria-expanded', 'false');
        }
      });
    }
  },

  // Smooth Scrolling
  setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      });
    });
  },

  // Modal System
  setupModals() {
    // Modal open triggers
    document.querySelectorAll('[data-modal-toggle]').forEach(trigger => {
      trigger.addEventListener('click', () => {
        const modalId = trigger.getAttribute('data-modal-toggle');
        this.openModal(modalId);
      });
    });

    // Modal close triggers
    document.querySelectorAll('[data-modal-close]').forEach(trigger => {
      trigger.addEventListener('click', () => {
        const modalId = trigger.getAttribute('data-modal-close');
        this.closeModal(modalId);
      });
    });

    // Close modal on backdrop click
    document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
      backdrop.addEventListener('click', (e) => {
        if (e.target === backdrop) {
          const modal = backdrop.closest('.modal');
          if (modal) {
            this.closeModal(modal.id);
          }
        }
      });
    });

    // Close modal on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const openModal = document.querySelector('.modal:not(.hidden)');
        if (openModal) {
          this.closeModal(openModal.id);
        }
      }
    });
  },

  // Open Modal
  openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.remove('hidden');
      modal.classList.add('animate-fade-in');
      document.body.style.overflow = 'hidden';
      
      // Focus trap
      const focusableElements = modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      if (focusableElements.length > 0) {
        focusableElements[0].focus();
      }
    }
  },

  // Close Modal
  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.add('hidden');
      modal.classList.remove('animate-fade-in');
      document.body.style.overflow = '';
    }
  },

  // Dropdown System
  setupDropdowns() {
    document.querySelectorAll('[data-dropdown-toggle]').forEach(trigger => {
      trigger.addEventListener('click', (e) => {
        e.stopPropagation();
        const dropdownId = trigger.getAttribute('data-dropdown-toggle');
        const dropdown = document.getElementById(dropdownId);
        
        if (dropdown) {
          // Close other dropdowns
          document.querySelectorAll('.dropdown-menu').forEach(menu => {
            if (menu.id !== dropdownId) {
              menu.classList.add('hidden');
            }
          });
          
          // Toggle current dropdown
          dropdown.classList.toggle('hidden');
        }
      });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', () => {
      document.querySelectorAll('.dropdown-menu').forEach(menu => {
        menu.classList.add('hidden');
      });
    });
  },

  // Search Functionality
  setupSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(input => {
      let searchTimeout;
      
      input.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        const query = e.target.value.trim();
        
        searchTimeout = setTimeout(() => {
          this.performSearch(query, input);
        }, 300);
      });
    });
  },

  // Perform Search
  performSearch(query, inputElement) {
    const searchResults = inputElement.closest('.search-container')?.querySelector('.search-results');
    
    if (!searchResults) return;
    
    if (query.length < 2) {
      searchResults.classList.add('hidden');
      return;
    }
    
    // Show loading state
    searchResults.innerHTML = '<div class="p-4 text-center text-gray-500">Searching...</div>';
    searchResults.classList.remove('hidden');
    
    // Simulate search (replace with actual search logic)
    setTimeout(() => {
      const mockResults = this.getMockSearchResults(query);
      this.displaySearchResults(mockResults, searchResults);
    }, 500);
  },

  // Mock Search Results (replace with actual API call)
  getMockSearchResults(query) {
    const allItems = [
      { type: 'resident', name: 'Juan Dela Cruz', id: '001' },
      { type: 'document', name: 'Barangay Certificate', id: '002' },
      { type: 'official', name: 'Maria Santos', id: '003' },
      { type: 'announcement', name: 'Community Meeting', id: '004' }
    ];
    
    return allItems.filter(item => 
      item.name.toLowerCase().includes(query.toLowerCase())
    );
  },

  // Display Search Results
  displaySearchResults(results, container) {
    if (results.length === 0) {
      container.innerHTML = '<div class="p-4 text-center text-gray-500">No results found</div>';
      return;
    }
    
    const resultsHTML = results.map(result => `
      <div class="p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0">
        <div class="flex items-center space-x-3">
          <span class="badge badge-primary">${result.type}</span>
          <span class="text-gray-900">${result.name}</span>
        </div>
      </div>
    `).join('');
    
    container.innerHTML = resultsHTML;
  },

  // Initialize Components
  initializeComponents() {
    this.initializeTabs();
    this.initializeTooltips();
    this.initializeAnimations();
    this.initializeDataTables();
  },

  // Tab System
  initializeTabs() {
    document.querySelectorAll('[data-tab-toggle]').forEach(tab => {
      tab.addEventListener('click', () => {
        const tabId = tab.getAttribute('data-tab-toggle');
        const tabGroup = tab.closest('.tab-group');
        
        if (tabGroup) {
          // Remove active class from all tabs and panels
          tabGroup.querySelectorAll('[data-tab-toggle]').forEach(t => {
            t.classList.remove('active');
            t.classList.add('text-gray-500');
            t.classList.remove('text-primary-600', 'border-primary-600');
          });
          
          tabGroup.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.add('hidden');
          });
          
          // Add active class to clicked tab
          tab.classList.add('active', 'text-primary-600', 'border-primary-600');
          tab.classList.remove('text-gray-500');
          
          // Show corresponding panel
          const targetPanel = document.getElementById(tabId);
          if (targetPanel) {
            targetPanel.classList.remove('hidden');
          }
        }
      });
    });
  },

  // Tooltip System
  initializeTooltips() {
    document.querySelectorAll('[data-tooltip]').forEach(element => {
      const tooltip = document.createElement('div');
      tooltip.className = 'tooltip absolute z-50 px-2 py-1 text-xs text-white bg-gray-900 rounded shadow-lg opacity-0 pointer-events-none transition-opacity duration-200';
      tooltip.textContent = element.getAttribute('data-tooltip');
      
      element.appendChild(tooltip);
      
      element.addEventListener('mouseenter', () => {
        tooltip.classList.remove('opacity-0');
        tooltip.classList.add('opacity-100');
      });
      
      element.addEventListener('mouseleave', () => {
        tooltip.classList.add('opacity-0');
        tooltip.classList.remove('opacity-100');
      });
    });
  },

  // Scroll Effects
  setupScrollEffects() {
    // Navbar background on scroll
    const navbar = document.querySelector('.navbar-scroll');
    if (navbar) {
      window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
          navbar.classList.add('bg-white', 'shadow-md');
          navbar.classList.remove('bg-transparent');
        } else {
          navbar.classList.remove('bg-white', 'shadow-md');
          navbar.classList.add('bg-transparent');
        }
      });
    }

    // Intersection Observer for animations
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-fade-in');
        }
      });
    }, observerOptions);

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
      observer.observe(el);
    });
  },

  // Animation Utilities
  initializeAnimations() {
    // Counter animations
    this.animateCounters();
    
    // Stagger animations for lists
    this.staggerAnimations();
  },

  // Counter Animation
  animateCounters() {
    document.querySelectorAll('.counter').forEach(counter => {
      const target = parseInt(counter.getAttribute('data-target'));
      const duration = parseInt(counter.getAttribute('data-duration')) || 2000;
      const increment = target / (duration / 16);
      let current = 0;

      const updateCounter = () => {
        current += increment;
        if (current < target) {
          counter.textContent = Math.floor(current);
          requestAnimationFrame(updateCounter);
        } else {
          counter.textContent = target;
        }
      };

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            updateCounter();
            observer.unobserve(counter);
          }
        });
      });

      observer.observe(counter);
    });
  },

  // Stagger Animations
  staggerAnimations() {
    document.querySelectorAll('.stagger-animation').forEach(container => {
      const items = container.querySelectorAll('.stagger-item');
      
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            items.forEach((item, index) => {
              setTimeout(() => {
                item.classList.add('animate-slide-up');
              }, index * 100);
            });
            observer.unobserve(container);
          }
        });
      });

      observer.observe(container);
    });
  },

  // Form Validation
  setupFormValidation() {
    document.querySelectorAll('form[data-validate]').forEach(form => {
      form.addEventListener('submit', (e) => {
        if (!this.validateForm(form)) {
          e.preventDefault();
        }
      });

      // Real-time validation
      form.querySelectorAll('input, textarea, select').forEach(field => {
        field.addEventListener('blur', () => {
          this.validateField(field);
        });
      });
    });
  },

  // Validate Form
  validateForm(form) {
    let isValid = true;
    const fields = form.querySelectorAll('input, textarea, select');
    
    fields.forEach(field => {
      if (!this.validateField(field)) {
        isValid = false;
      }
    });
    
    return isValid;
  },

  // Validate Field
  validateField(field) {
    const value = field.value.trim();
    const rules = field.getAttribute('data-rules')?.split('|') || [];
    let isValid = true;
    let errorMessage = '';

    // Remove existing error styles
    field.classList.remove('border-red-500');
    const existingError = field.parentNode.querySelector('.error-message');
    if (existingError) {
      existingError.remove();
    }

    // Validation rules
    rules.forEach(rule => {
      if (!isValid) return;

      if (rule === 'required' && !value) {
        isValid = false;
        errorMessage = 'This field is required';
      } else if (rule === 'email' && value && !this.isValidEmail(value)) {
        isValid = false;
        errorMessage = 'Please enter a valid email address';
      } else if (rule.startsWith('min:')) {
        const minLength = parseInt(rule.split(':')[1]);
        if (value && value.length < minLength) {
          isValid = false;
          errorMessage = `Minimum ${minLength} characters required`;
        }
      } else if (rule.startsWith('max:')) {
        const maxLength = parseInt(rule.split(':')[1]);
        if (value && value.length > maxLength) {
          isValid = false;
          errorMessage = `Maximum ${maxLength} characters allowed`;
        }
      }
    });

    // Display error if invalid
    if (!isValid) {
      field.classList.add('border-red-500');
      const errorDiv = document.createElement('div');
      errorDiv.className = 'error-message text-red-500 text-sm mt-1';
      errorDiv.textContent = errorMessage;
      field.parentNode.appendChild(errorDiv);
    }

    return isValid;
  },

  // Email validation utility
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },

  // Data Tables
  initializeDataTables() {
    document.querySelectorAll('.data-table').forEach(table => {
      this.enhanceTable(table);
    });
  },

  // Enhance Table
  enhanceTable(table) {
    // Add search functionality
    const searchInput = table.parentNode.querySelector('.table-search');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        this.filterTable(table, e.target.value);
      });
    }

    // Add sorting functionality
    table.querySelectorAll('th[data-sort]').forEach(header => {
      header.addEventListener('click', () => {
        const column = header.getAttribute('data-sort');
        this.sortTable(table, column);
      });
    });
  },

  // Filter Table
  filterTable(table, query) {
    const rows = table.querySelectorAll('tbody tr');
    const searchTerm = query.toLowerCase();

    rows.forEach(row => {
      const text = row.textContent.toLowerCase();
      if (text.includes(searchTerm)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  },

  // Sort Table
  sortTable(table, column) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const columnIndex = Array.from(table.querySelectorAll('th')).findIndex(
      th => th.getAttribute('data-sort') === column
    );

    rows.sort((a, b) => {
      const aValue = a.cells[columnIndex].textContent.trim();
      const bValue = b.cells[columnIndex].textContent.trim();
      
      if (!isNaN(aValue) && !isNaN(bValue)) {
        return parseFloat(aValue) - parseFloat(bValue);
      }
      
      return aValue.localeCompare(bValue);
    });

    rows.forEach(row => tbody.appendChild(row));
  },

  // Utility Functions
  utils: {
    // Debounce function
    debounce(func, wait) {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    },

    // Throttle function
    throttle(func, limit) {
      let inThrottle;
      return function(...args) {
        if (!inThrottle) {
          func.apply(this, args);
          inThrottle = true;
          setTimeout(() => inThrottle = false, limit);
        }
      };
    },

    // Format currency
    formatCurrency(amount) {
      return new Intl.NumberFormat('en-PH', {
        style: 'currency',
        currency: 'PHP'
      }).format(amount);
    },

    // Format date
    formatDate(date) {
      return new Intl.DateTimeFormat('en-PH', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }).format(new Date(date));
    },

    // Copy to clipboard
    async copyToClipboard(text) {
      try {
        await navigator.clipboard.writeText(text);
        this.showNotification('Copied to clipboard!', 'success');
      } catch (err) {
        console.error('Failed to copy text: ', err);
      }
    },

    // Show notification
    showNotification(message, type = 'info') {
      const notification = document.createElement('div');
      notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg max-w-sm animate-slide-down alert alert-${type}`;
      notification.textContent = message;
      
      document.body.appendChild(notification);
      
      setTimeout(() => {
        notification.remove();
      }, 3000);
    }
  }
};

// Alpine.js Page Functions
window.aboutPage = function() {
  return {
    activeTab: 'history',
    stats: {
      population: 1234,
      households: 456,
      area: '2.5',
      established: 1892
    },
    init() {
      console.log('About page initialized');
    },
    switchTab(tab) {
      this.activeTab = tab;
    }
  };
};

window.servicesPage = function() {
  return {
    selectedCategory: 'all',
    searchQuery: '',
    services: [
      { id: 1, name: 'Barangay Certificate', category: 'certificates', description: 'Official residency certificate', fee: 50, processing: '1-2 days' },
      { id: 2, name: 'Business Permit', category: 'permits', description: 'Business operation permit', fee: 200, processing: '3-5 days' },
      { id: 3, name: 'Barangay Clearance', category: 'clearances', description: 'Character clearance document', fee: 30, processing: '1 day' },
      { id: 4, name: 'Indigency Certificate', category: 'certificates', description: 'Certificate of indigency', fee: 25, processing: '1 day' }
    ],
    init() {
      console.log('Services page initialized');
    },
    get filteredServices() {
      let filtered = this.services;
      
      if (this.selectedCategory !== 'all') {
        filtered = filtered.filter(service => service.category === this.selectedCategory);
      }
      
      if (this.searchQuery) {
        filtered = filtered.filter(service => 
          service.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          service.description.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
      
      return filtered;
    },
    filterByCategory(category) {
      this.selectedCategory = category;
    }
  };
};

window.contactPage = function() {
  return {
    form: {
      name: '',
      email: '',
      subject: '',
      message: ''
    },
    isSubmitting: false,
    init() {
      console.log('Contact page initialized');
    },
    async submitForm() {
      this.isSubmitting = true;
      
      // Simulate form submission
      setTimeout(() => {
        iSerbisyo.utils.showNotification('Message sent successfully!', 'success');
        this.form = { name: '', email: '', subject: '', message: '' };
        this.isSubmitting = false;
      }, 1000);
    }
  };
};

window.officialsPage = function() {
  return {
    selectedOfficial: null,
    officials: [
      {
        id: 1,
        name: 'Juan Dela Cruz',
        position: 'Barangay Captain',
        term: '2022-2025',
        photo: 'https://via.placeholder.com/300x300',
        bio: 'Leading the community with dedication and transparency for the past 6 years.',
        achievements: ['Infrastructure Development', 'Peace and Order', 'Youth Programs']
      },
      {
        id: 2,
        name: 'Maria Santos',
        position: 'Kagawad - Health',
        term: '2022-2025',
        photo: 'https://via.placeholder.com/300x300',
        bio: 'Dedicated to improving community health and wellness programs.',
        achievements: ['Health Center Upgrade', 'Vaccination Programs', 'Senior Citizen Care']
      }
    ],
    init() {
      console.log('Officials page initialized');
    },
    selectOfficial(official) {
      this.selectedOfficial = official;
    }
  };
};

window.announcementsPage = function() {
  return {
    selectedCategory: 'all',
    announcements: [
      {
        id: 1,
        title: 'Community Meeting Schedule',
        category: 'meetings',
        date: '2025-09-25',
        content: 'Monthly community meeting will be held this Friday at 7 PM.',
        urgent: false
      },
      {
        id: 2,
        title: 'Road Maintenance Advisory',
        category: 'infrastructure',
        date: '2025-09-23',
        content: 'Main road will be closed for maintenance from 8 AM to 5 PM.',
        urgent: true
      }
    ],
    init() {
      console.log('Announcements page initialized');
    },
    get filteredAnnouncements() {
      if (this.selectedCategory === 'all') {
        return this.announcements;
      }
      return this.announcements.filter(announcement => announcement.category === this.selectedCategory);
    },
    filterByCategory(category) {
      this.selectedCategory = category;
    }
  };
};

window.loginForm = function() {
  return {
    form: {
      username: '',
      password: '',
      remember: false
    },
    showPassword: false,
    loading: false,
    errors: {},
    init() {
      console.log('Login form initialized');
    },
    async handleSubmit() {
      this.errors = {};
      this.loading = true;
      
      // Basic validation
      if (!this.form.username) {
        this.errors.username = 'Username is required';
      }
      if (!this.form.password) {
        this.errors.password = 'Password is required';
      }
      
      if (Object.keys(this.errors).length > 0) {
        this.loading = false;
        return;
      }
      
      // Simulate login
      setTimeout(() => {
        if (this.form.username === 'admin' && this.form.password === 'password') {
          window.location.href = 'dashboard.html';
        } else {
          this.errors.username = 'Invalid credentials';
          this.loading = false;
        }
      }, 1000);
    }
  };
};

window.dashboard = function() {
  return {
    sidebarOpen: false,
    currentPage: 'dashboard',
    stats: {
      totalResidents: 1234,
      pendingRequests: 23,
      completedRequests: 156,
      activeOfficials: 12,
      completedDocuments: 156,
      monthlyRevenue: 45678,
      notifications: 5
    },
    chartInstance: null,
    recentActivities: [
      {
        id: 1,
        type: 'approval',
        title: 'Barangay Certificate approved',
        subtitle: 'for Juan Dela Cruz',
        time: '2 minutes ago',
        icon: 'check',
        color: 'green'
      },
      {
        id: 2,
        type: 'registration',
        title: 'New resident registered',
        subtitle: 'Maria Santos',
        time: '15 minutes ago',
        icon: 'user',
        color: 'blue'
      },
      {
        id: 3,
        type: 'request',
        title: 'Business Permit requested',
        subtitle: 'by Pedro Reyes',
        time: '1 hour ago',
        icon: 'document',
        color: 'yellow'
      }
    ],
    
    init() {
      console.log('Dashboard initialized');
      this.loadDashboardData();
      this.initChart();
      this.startRealTimeUpdates();
    },
    
    loadDashboardData() {
      // Simulate data loading with animation
      this.animateStats();
    },
    
    animateStats() {
      // Animate the stats counters
      const statsElements = document.querySelectorAll('.stat-number');
      statsElements.forEach(element => {
        const target = parseInt(element.textContent.replace(/[^0-9]/g, ''));
        this.animateCounter(element, 0, target, 2000);
      });
    },
    
    animateCounter(element, start, end, duration) {
      const increment = (end - start) / (duration / 16);
      let current = start;
      
      const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
          current = end;
          clearInterval(timer);
        }
        
        // Format the number based on the type
        let formattedValue = Math.floor(current);
        if (element.dataset.type === 'currency') {
          formattedValue = '₱' + formattedValue.toLocaleString();
        } else {
          formattedValue = formattedValue.toLocaleString();
        }
        
        element.textContent = formattedValue;
      }, 16);
    },
    
    initChart() {
      this.$nextTick(() => {
        const canvas = document.getElementById('requestsChart');
        if (canvas && typeof Chart !== 'undefined') {
          // Destroy existing chart if it exists
          if (this.chartInstance) {
            this.chartInstance.destroy();
          }
          
          const ctx = canvas.getContext('2d');
          this.chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
              labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
              datasets: [{
                label: 'Document Requests',
                data: [65, 59, 80, 81, 56, 77, 88, 92, 85],
                borderColor: 'rgb(59, 130, 246)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4,
                fill: true,
                pointBackgroundColor: 'rgb(59, 130, 246)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  display: false
                }
              },
              scales: {
                x: {
                  grid: {
                    display: false
                  },
                  ticks: {
                    font: {
                      size: 12
                    }
                  }
                },
                y: {
                  beginAtZero: true,
                  grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                  },
                  ticks: {
                    font: {
                      size: 12
                    }
                  }
                }
              },
              elements: {
                point: {
                  hoverRadius: 8
                }
              }
            }
          });
        } else {
          console.warn('Chart.js not loaded or canvas element not found');
        }
      });
    },
    
    startRealTimeUpdates() {
      // Simulate real-time updates every 30 seconds
      setInterval(() => {
        this.updateStats();
        this.addRandomActivity();
      }, 30000);
    },
    
    updateStats() {
      // Simulate random stat changes
      const changes = {
        totalResidents: Math.floor(Math.random() * 5),
        pendingRequests: Math.floor(Math.random() * 3) - 1,
        completedDocuments: Math.floor(Math.random() * 10),
        monthlyRevenue: Math.floor(Math.random() * 1000)
      };
      
      Object.keys(changes).forEach(key => {
        this.stats[key] += changes[key];
        if (this.stats[key] < 0) this.stats[key] = 0;
      });
    },
    
    addRandomActivity() {
      const activities = [
        {
          type: 'approval',
          title: 'Certificate approved',
          subtitle: 'for New Resident',
          icon: 'check',
          color: 'green'
        },
        {
          type: 'request',
          title: 'New document requested',
          subtitle: 'Barangay Clearance',
          icon: 'document',
          color: 'yellow'
        }
      ];
      
      const newActivity = {
        ...activities[Math.floor(Math.random() * activities.length)],
        id: Date.now(),
        time: 'Just now'
      };
      
      this.recentActivities.unshift(newActivity);
      if (this.recentActivities.length > 5) {
        this.recentActivities.pop();
      }
    },
    
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen;
    },
    
    switchPage(page) {
      this.currentPage = page;
      if (this.sidebarOpen) {
        this.sidebarOpen = false; // Close sidebar on mobile after navigation
      }
    },
    
    generateReport() {
      // Simulate report generation
      iSerbisyo.utils.showNotification('Generating monthly report...', 'info');
      
      setTimeout(() => {
        iSerbisyo.utils.showNotification('Report generated successfully!', 'success');
      }, 2000);
    },
    
    getPageTitle() {
      const pageTitles = {
        dashboard: 'Dashboard',
        residents: 'Residents Management',
        documents: 'Document Requests',
        officials: 'Barangay Officials',
        announcements: 'Announcements',
        reports: 'Reports',
        settings: 'Settings'
      };
      return pageTitles[this.currentPage] || 'Dashboard';
    },
    
    refreshData() {
      // Simulate data refresh
      iSerbisyo.utils.showNotification('Refreshing data...', 'info');
      this.loadDashboardData();
      
      setTimeout(() => {
        iSerbisyo.utils.showNotification('Data refreshed successfully!', 'success');
      }, 1000);
    }
  };
};

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  iSerbisyo.init();
});

// Export for use in other modules
window.iSerbisyo = iSerbisyo;