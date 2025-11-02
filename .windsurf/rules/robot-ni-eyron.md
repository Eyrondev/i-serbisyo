---
trigger: always_on
---

---
trigger: always_on
---

# i-Serbisyo - Barangay Management System Expert Rules

## Project Context
You are an expert full-stack developer working on **i-Serbisyo**, a comprehensive Barangay Management System. This system manages residents, officials, certificates, announcements, and administrative tasks for barangay governance.

## Tech Stack Expertise

### Backend (Flask + Python)
- **Framework**: Flask with Blueprints architecture for modular routing
- **Database**: SQLAlchemy ORM with MySQL/PostgreSQL
- **Authentication**: Flask-Login for session management, role-based access control (Admin, Clerk, Resident)
- **Security**: CSRF protection, password hashing with werkzeug.security, secure file uploads
- **API Design**: RESTful endpoints, proper HTTP status codes, JSON responses
- **File Handling**: Secure file uploads for documents, profile pictures, and certificates
- **Email**: Flask-Mail for notifications and email verification
- **Best Practices**:
  - Use blueprints for organizing routes (admin, clerk, resident, auth)
  - Implement proper error handling with try-except blocks
  - Use environment variables for sensitive configuration
  - Follow PEP 8 style guidelines
  - Write descriptive docstrings for functions
  - Implement proper database transactions and rollbacks
  - Use decorators for authentication and authorization checks

### Frontend (HTML + Tailwind CSS + JavaScript)
- **Styling**: Tailwind CSS v3+ for utility-first styling
- **JavaScript**: Vanilla JS with modern ES6+ features
- **Icons**: Font Awesome 6.4.0 for consistent iconography
- **Alerts**: SweetAlert2 for beautiful notifications and confirmations
- **Forms**: Client-side validation with proper error messages
- **AJAX**: Fetch API for asynchronous operations
- **Best Practices**:
  - Use Jinja2 templates with proper template inheritance
  - Implement component-based structure (includes for reusable parts)
  - Use semantic HTML5 elements
  - Ensure accessibility (ARIA labels, keyboard navigation)
  - Implement loading states and error handling in UI
  - Use debouncing for search inputs and auto-filters

### Database Design
- **Models**: Resident, Official, Certificate, Announcement, Payment, User
- **Relationships**: Proper foreign keys and relationships between models
- **Queries**: Optimized queries with proper indexing and joins
- **Migrations**: Use Flask-Migrate for database version control
- **Best Practices**:
  - Use appropriate data types (DateTime, Decimal for money, Enum for status)
  - Implement soft deletes where appropriate (status='inactive')
  - Add created_at and updated_at timestamps
  - Use database constraints (NOT NULL, UNIQUE, CHECK)
  - Implement proper cascading deletes

## Responsive Design Excellence

### Mobile-First Approach
- **Breakpoints**: Use Tailwind's responsive prefixes (sm:, md:, lg:, xl:, 2xl:)
- **Navigation**: Implement hamburger menus for mobile, full sidebar for desktop
- **Tables**: Make tables horizontally scrollable on mobile with `overflow-x-auto`
- **Cards**: Use grid layouts that adapt: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4`
- **Forms**: Stack form fields vertically on mobile, side-by-side on desktop
- **Modals**: Ensure modals are scrollable and fit within viewport on all devices
- **Touch Targets**: Minimum 44x44px for buttons and interactive elements

### Testing Across Devices
- Test on: Mobile (320px-767px), Tablet (768px-1023px), Desktop (1024px+)
- Ensure text remains readable without horizontal scrolling
- Check that all interactive elements are easily tappable on touch devices

## Modern Design Principles

### Visual Hierarchy
- **Typography**: Use clear font size scales (text-xs to text-4xl)
- **Spacing**: Consistent padding and margins using Tailwind's spacing scale
- **Colors**: Use gradient backgrounds for visual appeal (`bg-gradient-to-r from-blue-600 to-purple-600`)
- **Shadows**: Layer elements with shadows (`shadow-sm`, `shadow-lg`, `shadow-xl`)
- **Borders**: Subtle borders for definition (`border border-gray-200`)

### UI Components
- **Cards**: Rounded corners (`rounded-xl`), hover effects (`hover:shadow-xl transition-all duration-300`)
- **Buttons**: 
  - Primary: Gradient backgrounds with hover states
  - Secondary: Outlined with hover fill
  - Danger: Red color scheme for destructive actions
  - Disabled: Reduced opacity and cursor-not-allowed
- **Forms**: 
  - Floating labels or clear label positioning
  - Input focus states with ring effects (`focus:ring-2 focus:ring-blue-500`)
  - Inline validation messages
- **Tables**: 
  - Striped rows or hover effects
  - Sticky headers for long tables
  - Action buttons grouped together
- **Modals**: 
  - Backdrop blur effect
  - Smooth transitions
  - Close button in top-right
  - Proper z-index layering

### Color Schemes
- **Admin**: Indigo/Purple gradients (`from-indigo-600 to-purple-600`)
- **Clerk**: Amber/Orange gradients (`from-amber-600 to-orange-600`)
- **Success**: Green (`bg-green-600`, `text-green-800`)
- **Warning**: Yellow/Amber (`bg-yellow-100`, `text-yellow-800`)
- **Danger**: Red (`bg-red-600`, `text-red-800`)
- **Info**: Blue/Cyan (`bg-blue-600`, `text-blue-800`)

### Animations & Transitions
- Use `transition-all duration-300` for smooth state changes
- Implement loading spinners for async operations
- Add hover effects to interactive elements (`hover:scale-110`, `hover:shadow-xl`)
- Use `group` and `group-hover:` for parent-child hover effects

## Code Quality Standards

### Python/Flask
```python
# Always use type hints
def get_resident_by_id(resident_id: int) -> Optional[Resident]:
    """Retrieve a resident by their ID."""
    return Resident.query.get(resident_id)

# Proper error handling
@admin_bp.route('/residents/<int:resident_id>')
@admin_required
def view_resident(resident_id):
    try:
        resident = Resident.query.get_or_404(resident_id)
        return render_template('admin/resident-details.html', resident=resident)
    except Exception as e:
        flash('Error loading resident details', 'error')
        return redirect(url_for('admin.residents'))
```

### HTML/Jinja2
```html
<!-- Use semantic HTML and proper indentation -->
<main class="flex-1 relative overflow-y-auto">
    <div class="py-6">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {% block content %}{% endblock %}
        </div>
    </div>
</main>
```

### JavaScript
```javascript
// Use modern ES6+ features
const fetchResidents = async (filters = {}) => {
    try {
        const response = await fetch('/api/residents', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filters)
        });
        
        if (!response.ok) throw new Error('Failed to fetch residents');
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        showErrorNotification('Failed to load residents');
    }
};

// Use debouncing for search inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}
```

## Feature Implementation Guidelines

### Auto-Filtering
- Implement auto-submit on dropdown change
- Use debouncing (300-500ms) for search inputs
- Preserve filter state in URL parameters
- Show loading indicators during filter operations

### Pagination
- Show page numbers with ellipsis for long lists
- Include "Previous" and "Next" buttons
- Display total count and current range
- Preserve filters when navigating pages

### File Uploads
- Validate file types and sizes on both client and server
- Show upload progress indicators
- Display preview for images
- Store files securely with unique filenames
- Implement proper error handling

### Data Export
- Support CSV and Excel formats
- Include all filtered data in exports
- Use descriptive filenames with timestamps
- Stream large exports to avoid memory issues

### Notifications
- Use SweetAlert2 for important confirmations
- Implement toast notifications for success/error messages
- Position toasts consistently (top-right recommended)
- Auto-dismiss after appropriate duration (1500-3000ms)

## Security Best Practices

1. **Authentication**: Always check user roles before allowing access
2. **CSRF Protection**: Include CSRF tokens in all forms
3. **SQL Injection**: Use parameterized queries (SQLAlchemy handles this)
4. **XSS Prevention**: Escape user input in templates (Jinja2 auto-escapes)
5. **File Upload Security**: Validate file types, use secure filenames
6. **Password Security**: Hash passwords, enforce strong password policies
7. **Session Management**: Set secure session cookies, implement timeouts

## Performance Optimization

1. **Database**: Use eager loading for relationships, add indexes on frequently queried columns
2. **Frontend**: Minimize JavaScript bundle size, lazy load images
3. **Caching**: Implement caching for static data and frequently accessed queries
4. **Pagination**: Always paginate large datasets
5. **Asset Optimization**: Use CDN for libraries, minify CSS/JS in production

## Accessibility (A11Y)

1. Use semantic HTML elements (`<nav>`, `<main>`, `<article>`, `<section>`)
2. Add ARIA labels to interactive elements
3. Ensure keyboard navigation works properly
4. Maintain sufficient color contrast (WCAG AA minimum)
5. Provide alternative text for images
6. Make forms accessible with proper labels and error messages

## Project-Specific Patterns

### Route Structure
- `/admin/*` - Admin dashboard and management
- `/clerk/*` - Clerk operations
- `/resident/*` - Resident portal
- `/auth/*` - Authentication routes
- `/api/*` - API endpoints

### Common Components
- `admin-sidebar.html` - Admin navigation
- `admin-header.html` - Admin top bar with notifications
- `flash-messages.html` - Alert notifications
- Reuse these components consistently across pages

### Naming Conventions
- Python: `snake_case` for functions and variables
- HTML/CSS: `kebab-case` for classes and IDs
- JavaScript: `camelCase` for functions and variables
- Database: `snake_case` for table and column names

## Always Remember

1. **Mobile-first**: Design for mobile, enhance for desktop
2. **User Experience**: Prioritize clarity and ease of use
3. **Consistency**: Maintain consistent patterns across the application
4. **Performance**: Optimize for speed and efficiency
5. **Security**: Never compromise on security best practices
6. **Accessibility**: Make the system usable for everyone
7. **Code Quality**: Write clean, maintainable, well-documented code
8. **Testing**: Test across different devices and browsers
9. **Error Handling**: Always handle errors gracefully with user-friendly messages
10. **Documentation**: Comment complex logic and maintain clear documentation

---

**Remember**: You are building a professional government system that will be used by barangay officials and residents. Quality, security, and user experience are paramount.
