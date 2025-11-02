# GitHub Copilot Instructions for i-Serbisyo - Barangay Management System

## Project Overview
You are an expert full-stack developer working on **i-Serbisyo**, a modern Barangay Management System. This project streamlines municipal services, resident management, certificate processing, and community administration for Philippine barangays.

## Core Technology Stack
- **Backend**: Flask (Python 3.x) with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Tailwind CSS, Vanilla JavaScript
- **Database**: MySQL/MariaDB
- **Authentication**: Flask-Login with role-based access control (Admin, Clerk, Resident)
- **Email**: Flask-Mail for notifications and password resets
- **File Handling**: Document uploads, profile pictures, certificate generation

## Development Standards

### Python/Flask Best Practices
- Follow PEP 8 style guidelines with 4-space indentation
- Use type hints for function parameters and return values
- Implement proper error handling with try-except blocks and flash messages
- Use blueprint architecture for route organization (auth, admin, clerk, resident, public)
- Implement database transactions with proper rollback on errors
- Use environment variables for sensitive configuration (via python-dotenv)
- Apply decorators for authentication and authorization checks
- Write docstrings for all functions and classes
- Use SQLAlchemy ORM patterns with proper session management
- Implement pagination for large data sets
- Sanitize user inputs to prevent SQL injection and XSS attacks

### Frontend Development Standards
- **Tailwind CSS**: Use utility-first approach with responsive design classes
- **Responsive Design**: Mobile-first approach (sm:, md:, lg:, xl:, 2xl: breakpoints)
- **Modern UI/UX**: Clean, intuitive interfaces with proper spacing, typography, and color schemes
- **Accessibility**: Semantic HTML, ARIA labels, keyboard navigation support
- **JavaScript**: Use ES6+ features, async/await for API calls, modular code organization
- **Component Architecture**: Reusable components in templates/components/
- **Loading States**: Implement loading indicators for async operations
- **Form Validation**: Client-side validation with user-friendly error messages
- **Dark Mode**: Consider dark mode compatibility where applicable

### Responsive Design Guidelines
```css
/* Mobile First - Base styles for mobile devices */
.container { /* Mobile styles */ }

/* Tablet and up */
@media (min-width: 640px) { /* sm: */ }
@media (min-width: 768px) { /* md: */ }

/* Desktop and up */
@media (min-width: 1024px) { /* lg: */ }
@media (min-width: 1280px) { /* xl: */ }
@media (min-width: 1536px) { /* 2xl: */ }
```

### Database Best Practices
- Use proper foreign key relationships and cascade rules
- Index frequently queried columns for performance
- Implement soft deletes where appropriate
- Use database migrations for schema changes
- Normalize data to reduce redundancy
- Add timestamps (created_at, updated_at) to all tables
- Use transactions for multi-step operations
- Implement proper backup and restore procedures

### Security Requirements
- Hash passwords using bcrypt or werkzeug.security
- Implement CSRF protection on all forms
- Validate and sanitize all user inputs
- Use parameterized queries to prevent SQL injection
- Implement rate limiting on authentication endpoints
- Secure file upload handling (validate file types, sizes, and scan for malware)
- Use HTTPS in production
- Implement proper session management
- Log security events (failed logins, permission denials)

### Code Organization
```
i-serbisyo/
├── routes/          # Blueprint modules (auth, admin, clerk, resident, public)
├── templates/       # Jinja2 templates
│   ├── admin/      # Admin dashboard views
│   ├── clerk/      # Clerk dashboard views
│   ├── residents/  # Resident dashboard views
│   ├── public/     # Public-facing pages
│   ├── components/ # Reusable UI components
│   └── errors/     # Error pages
├── static/
│   ├── css/        # Tailwind and custom styles
│   ├── js/         # JavaScript modules
│   ├── images/     # Static images
│   └── uploads/    # User-generated content
├── database/       # SQL schemas and migrations
├── models.py       # SQLAlchemy models
├── config.py       # Configuration management
├── utils.py        # Helper functions
├── email_utils.py  # Email handling
└── app.py          # Application factory
```

### User Roles & Permissions
1. **Admin**: Full system access, user management, system settings, activity logs
2. **Clerk**: Certificate processing, resident verification, document management
3. **Resident**: Profile management, certificate requests, announcements viewing
4. **Public**: Registration, information viewing, contact forms

### Modern Design Principles
- **Clean & Minimal**: Avoid clutter, use white space effectively
- **Consistent**: Maintain uniform color schemes, typography, and spacing
- **Intuitive Navigation**: Clear menu structures, breadcrumbs, search functionality
- **Visual Hierarchy**: Use size, color, and spacing to guide user attention
- **Microinteractions**: Subtle animations for buttons, transitions, and feedback
- **Card-based Layouts**: Use cards for content grouping and organization
- **Color Palette**: Professional, accessible colors with proper contrast ratios
- **Typography**: Readable font sizes (16px+ for body text), clear hierarchy
- **Icons**: Use consistent icon sets (Heroicons, Font Awesome, or similar)
- **Feedback**: Provide immediate visual feedback for user actions

### Tailwind CSS Patterns
```html
<!-- Modern Card Component -->
<div class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 p-6">
  <!-- Card content -->
</div>

<!-- Responsive Grid -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  <!-- Grid items -->
</div>

<!-- Modern Button -->
<button class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200">
  Action
</button>

<!-- Responsive Navigation -->
<nav class="hidden md:flex space-x-4">
  <!-- Desktop menu -->
</nav>
<button class="md:hidden" onclick="toggleMobileMenu()">
  <!-- Mobile menu toggle -->
</button>
```

### Flask Route Patterns
```python
@blueprint.route('/endpoint', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def view_function():
    """
    Brief description of the function.
    
    Returns:
        Response: Rendered template or JSON response
    """
    try:
        # Implementation
        return render_template('template.html', data=data)
    except Exception as e:
        flash('Error message', 'error')
        return redirect(url_for('fallback.route'))
```

### API Response Format
```python
# Success response
return jsonify({
    'success': True,
    'message': 'Operation successful',
    'data': result_data
}), 200

# Error response
return jsonify({
    'success': False,
    'message': 'Error description',
    'errors': validation_errors
}), 400
```

### Testing Guidelines
- Write unit tests for critical functions
- Test all user roles and permissions
- Test form validation and error handling
- Test responsive design on multiple devices
- Perform security testing (OWASP Top 10)
- Test database transactions and rollbacks
- Test email sending functionality

### Performance Optimization
- Lazy load images and components
- Minify CSS and JavaScript in production
- Use database connection pooling
- Implement caching for frequently accessed data
- Optimize database queries (avoid N+1 queries)
- Use CDN for static assets
- Compress responses with gzip
- Implement pagination for large datasets

### Documentation Standards
- Comment complex logic and business rules
- Maintain README.md with setup instructions
- Document API endpoints and parameters
- Keep USER_MANUAL.md updated for end users
- Document environment variables in .env.example
- Include inline comments for non-obvious code

### Git Commit Message Format
```
feat: Add certificate generation feature
fix: Resolve pagination bug in residents list
style: Update responsive design for mobile devices
refactor: Improve database query performance
docs: Update API documentation
chore: Update dependencies
```

## Feature-Specific Guidelines

### Certificate Management
- Generate PDF certificates with proper formatting
- Implement digital signatures where applicable
- Track certificate status (pending, approved, issued, rejected)
- Store certificate templates in the database or filesystem
- Implement certificate number generation system

### Document Upload
- Validate file types (PDF, JPEG, PNG only)
- Limit file sizes (max 5MB per file)
- Generate unique filenames to prevent conflicts
- Store files securely with access controls
- Implement virus scanning for uploaded files

### Dashboard Analytics
- Display key metrics with visual charts
- Implement real-time or cached data updates
- Use responsive chart libraries (Chart.js, ApexCharts)
- Provide data export functionality (CSV, PDF)
- Show trends and comparisons over time

### Notification System
- Email notifications for important events
- In-app notifications for logged-in users
- SMS notifications (if integrated)
- Push notifications (if applicable)
- Notification preferences per user

## When Generating Code
1. **Always consider mobile responsiveness** - Use Tailwind responsive utilities
2. **Follow the existing project structure** - Match file organization patterns
3. **Implement proper error handling** - Never leave try blocks empty
4. **Add user feedback** - Use flash messages or toast notifications
5. **Validate inputs** - Both client-side and server-side validation
6. **Check permissions** - Verify user roles before allowing actions
7. **Write clean, readable code** - Self-documenting with clear variable names
8. **Optimize for performance** - Efficient queries and minimal HTTP requests
9. **Ensure accessibility** - WCAG 2.1 AA compliance
10. **Test across devices** - Ensure functionality on all screen sizes

## Modern Design Trends to Follow
- Glassmorphism effects (frosted glass backgrounds)
- Neumorphism (soft UI elements)
- Gradient backgrounds and buttons
- Smooth scroll animations
- Skeleton loading screens
- Empty states with illustrations
- Contextual help and tooltips
- Progress indicators for multi-step processes
- Confirmation dialogs for destructive actions
- Success animations after completing actions

## Prohibited Practices
- ❌ Inline styles (use Tailwind classes)
- ❌ Hardcoded sensitive data (use environment variables)
- ❌ Direct SQL queries (use SQLAlchemy ORM)
- ❌ Plain text passwords
- ❌ Unvalidated user inputs
- ❌ Missing error handling
- ❌ Non-responsive designs
- ❌ Poor accessibility (missing alt tags, labels)
- ❌ Inconsistent naming conventions
- ❌ Uncommitted debugging code

## Remember
You are building a professional, production-ready barangay management system that will be used by real government officials and residents. Prioritize **security, reliability, user experience, and maintainability** in every line of code you write.
