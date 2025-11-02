# 🏘️ i-Serbisyo - Barangay Management System

A comprehensive, modern barangay management system built with Flask, MySQL, and Tailwind CSS. Designed to streamline community services, manage residents, process certificates, and facilitate communication between barangay officials and residents.

---

## ✨ Features

### 👥 Multi-Role Access System
- **Super Admin** - Full system control and configuration
- **Admin** - Manage residents, certificates, announcements, and officials
- **Clerk** - Process certificate requests, manage payments, and assist residents
- **Resident** - Request certificates, view announcements, track requests

### 📋 Certificate Management
- **Online Certificate Requests** - Residents can request certificates online
- **Dynamic Certificate Types** - Managed through database (Barangay Clearance, Indigency, Residency, Business Permit)
- **Payment Tracking** - Complete payment processing and tracking system
- **Status Workflow** - Pending → Processing → Ready → Claimed
- **Digital Records** - Paperless certificate management

### 🏠 Resident Management
- **Complete Resident Profiles** - Personal info, address, family details
- **Purok/Zone Organization** - Residents grouped by purok
- **Voter Registration Tracking** - Track registered voters
- **Status Management** - Pending, Approved, Rejected residents
- **Document Uploads** - Profile pictures and supporting documents

### 📢 Announcements & Communication
- **Public Announcements** - System-wide announcements with priority levels
- **Category Management** - Events, Notices, Emergency, Health, Services
- **Featured & Pinned Posts** - Highlight important announcements
- **View Tracking** - Monitor announcement engagement

### 👔 Officials Directory
- **Official Profiles** - Complete information for barangay officials
- **Position Hierarchy** - Captain, Councilors, SK Chairman, Secretary, Treasurer
- **Term Management** - Track official terms and status
- **Photo Gallery** - Official photos and contact information

### 📊 Dashboard & Analytics
- **Real-time Statistics** - Residents, certificates, payments, activities
- **Monthly Revenue Charts** - Track certificate fees and payments
- **Activity Monitoring** - System activity logs and user actions
- **Performance Metrics** - Request processing times and completion rates

### 🔒 Security & Privacy
- **Secure Authentication** - Password hashing with Werkzeug
- **Role-based Access Control** - Fine-grained permissions
- **Session Management** - Secure session handling
- **Activity Logging** - Track all user actions with IP and timestamp
- **Data Protection** - Secure file uploads and data validation

### ⚙️ System Settings
- **Maintenance Mode** - Disable public access for maintenance
- **Registration Control** - Enable/disable resident registration
- **Barangay Information** - Customizable barangay details
- **Email Configuration** - Notification system setup

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL Server (XAMPP recommended)
- Web browser

### Installation

1. **Clone the Repository**
```bash
git clone <repository-url>
cd new-iserbisyo
```

2. **Create Virtual Environment**
```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Database**
- Start XAMPP MySQL server
- Create database: `iserbisyo_db`
- Import SQL file from `database/iserbisyo_db.sql`

5. **Configure Environment**
Create `.env` file in root directory:
```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
DATABASE_URL=mysql://root:@localhost/iserbisyo_db
```

6. **Run Application**
```bash
python app.py
```

7. **Access the Application**
Open browser: `http://localhost:5000`

---

## 🔑 Default Accounts

| Role | Username | Email | Password |
|------|----------|-------|----------|
| Super Admin | superadmin | superadmin@iserbisyo.com | admin123 |
| Admin | admin | admin@iserbisyo.com | admin123 |
| Clerk | clerk | clerk@iserbisyo.com | clerk123 |
| Resident | resident | resident@iserbisyo.com | resident123 |

**⚠️ Change these passwords immediately after first login!**

---

## 📁 Project Structure

```
new-iserbisyo/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── models.py                   # Database models (13 models)
├── utils.py                    # Utility functions & decorators
├── activity_logger.py          # Activity logging system
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── routes/                     # Application routes (Blueprints)
│   ├── __init__.py            # Blueprint initialization
│   ├── auth.py                # Authentication routes
│   ├── admin.py               # Admin routes
│   ├── clerk.py               # Clerk routes
│   ├── resident.py            # Resident routes
│   └── public.py              # Public routes
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html              # Base template with inheritance
│   ├── admin/                 # Admin dashboard pages
│   │   ├── dashboard.html
│   │   ├── residents.html
│   │   ├── pending-residents.html
│   │   ├── certificates.html
│   │   ├── certificate-payment.html
│   │   ├── payment-list.html
│   │   ├── officials.html
│   │   ├── announcements.html
│   │   ├── blotter.html
│   │   ├── activity-log.html
│   │   └── settings.html
│   ├── clerk/                 # Clerk dashboard pages
│   │   ├── dashboard.html
│   │   ├── residents.html
│   │   ├── certificates.html
│   │   ├── announcements.html
│   │   └── settings.html
│   ├── residents/             # Resident portal pages
│   │   ├── dashboard.html
│   │   ├── certificates.html
│   │   ├── announcements.html
│   │   └── settings.html
│   ├── public/                # Public pages
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── about.html
│   │   ├── services.html
│   │   ├── announcements.html
│   │   ├── officials.html
│   │   ├── contact.html
│   │   ├── maintenance.html
│   │   └── registration-closed.html
│   ├── components/            # Reusable components
│   │   ├── admin-header.html
│   │   ├── admin-sidebar.html
│   │   ├── clerk-header.html
│   │   ├── clerk-sidebar.html
│   │   ├── resident-header.html
│   │   ├── resident-sidebar.html
│   │   ├── navigation.html
│   │   ├── footer.html
│   │   └── loading-screen.html
│   └── errors/                # Error pages
│       ├── 404.html
│       └── 500.html
│
├── static/                     # Static assets
│   ├── css/
│   │   └── main.css           # Custom styles
│   ├── js/
│   │   ├── main.js            # Main JavaScript
│   │   ├── navigation-loader.js
│   │   ├── component-loader.js
│   │   ├── admin-navigation.js
│   │   └── admin-component-loader.js
│   ├── images/                # Images and logos
│   │   ├── system-logo.png
│   │   ├── main-icon.png
│   │   ├── landing_page_bg.png
│   │   └── no-picture.jpg
│   └── uploads/               # User uploaded files
│       ├── profiles/          # Profile pictures
│       └── documents/         # Document uploads
│
└── database/
    └── iserbisyo_db.sql       # MySQL database schema & data
```

---

## 🗄️ Database Models

### Core Models
1. **User** - Authentication and user accounts
2. **Resident** - Resident profiles and information
3. **Certificate** - Certificate requests and records
4. **CertificateType** - Certificate type definitions
5. **Official** - Barangay officials directory
6. **Announcement** - Public announcements
7. **BlotterRecord** - Incident and blotter records
8. **SystemActivity** - Activity logging
9. **Payment** - Payment records and tracking
10. **SystemSettings** - System configuration
11. **BarangayInfo** - Barangay information
12. **ContactMessage** - Contact form messages
13. **PurokInfo** - Purok/zone information

---

## 🛣️ Route Structure

### Public Routes (`/`)
- `/` - Homepage
- `/login` - User login
- `/logout` - User logout
- `/about` - About barangay
- `/services` - Available services
- `/announcements` - View announcements
- `/officials` - Barangay officials
- `/contact` - Contact form
- `/register` - Resident registration

### Admin Routes (`/admin`)
- `/admin/dashboard` - Admin dashboard with statistics
- `/admin/residents` - Manage all residents
- `/admin/pending-residents` - Approve/reject resident applications
- `/admin/certificates` - Manage certificate requests
- `/admin/certificate-payment` - Process certificate payments
- `/admin/payment-list` - View all payments
- `/admin/officials` - Manage barangay officials
- `/admin/announcements` - Create and manage announcements
- `/admin/blotter` - Manage blotter records
- `/admin/activity-log` - View system activity logs
- `/admin/settings` - System settings and configuration

### Clerk Routes (`/clerk`)
- `/clerk/dashboard` - Clerk dashboard
- `/clerk/residents` - View residents
- `/clerk/pending-residents` - View pending residents
- `/clerk/certificates` - Process certificates
- `/clerk/certificate-payment` - Process payments
- `/clerk/payment-list` - View payments
- `/clerk/announcements` - View announcements
- `/clerk/officials` - View officials
- `/clerk/settings` - Clerk account settings

### Resident Routes (`/residents`)
- `/residents/dashboard` - Resident dashboard
- `/residents/certificates` - Request and track certificates
- `/residents/announcements` - View announcements
- `/residents/settings` - Account settings and password change

---

## 🎨 Technologies Used

### Backend
- **Flask 3.0+** - Python web framework
- **SQLAlchemy 2.0+** - SQL toolkit and ORM
- **PyMySQL** - MySQL database connector
- **Werkzeug** - Security utilities and password hashing
- **Jinja2** - Template engine

### Frontend
- **Tailwind CSS** - Utility-first CSS framework (CDN)
- **Font Awesome 6** - Icon library (CDN)
- **Vanilla JavaScript** - No heavy frameworks
- **Responsive Design** - Mobile-first approach

### Database
- **MySQL** - Relational database
- **XAMPP** - Local development environment

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Database Configuration
SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/iserbisyo_db'

# Session Configuration
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

# File Upload Configuration
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'}

# Email Configuration (Optional)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'

# Barangay Information
BARANGAY_NAME = 'Sample Barangay'
MUNICIPALITY = 'Sample Municipality'
PROVINCE = 'Sample Province'
```

### Environment Variables (`.env`)
```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
DATABASE_URL=mysql://root:@localhost/iserbisyo_db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

---

## 🔐 Security Features

- **Password Hashing** - Werkzeug secure password hashing
- **Session Management** - Secure session cookies
- **Role-based Access Control** - Decorators for route protection
- **CSRF Protection Ready** - Form security implementation
- **Input Validation** - Server-side validation utilities
- **Activity Logging** - Track all user actions with IP addresses
- **File Upload Security** - Extension and size validation
- **SQL Injection Protection** - SQLAlchemy ORM parameterization

---

## 📊 Key Features in Detail

### Certificate Processing Workflow
1. **Resident Request** - Submit certificate request online
2. **Admin/Clerk Review** - Review and validate request
3. **Processing** - Change status to "processing"
4. **Payment** - Move to payment list when ready
5. **Completion** - Mark as "ready for pickup"
6. **Claim** - Mark as "claimed" upon release

### Payment Management
- Multiple payment methods (Cash, GCash, Bank Transfer, Check, Online)
- Payment receipt generation
- Payment history tracking
- Revenue reports and analytics
- Certificate fee management through database

### Resident Management
- Comprehensive profile information
- Family composition tracking
- Voter registration status
- Emergency contact information
- Purok/zone assignment
- Document upload support
- Status workflow (Pending → Approved/Rejected)

### Announcement System
- Rich content management
- Category-based organization
- Priority levels (Low, Normal, High, Urgent)
- Featured and pinned announcements
- View count tracking
- Publication scheduling
- Expiry date management

---

## 📱 Responsive Design

The system is fully responsive and works on:
- 📱 Mobile phones (320px+)
- 📱 Tablets (768px+)
- 💻 Laptops (1024px+)
- 🖥️ Desktops (1280px+)
- 🖥️ Large screens (1920px+)

---

## 🛠️ Development

### Running in Development Mode
```bash
# Windows
set FLASK_ENV=development
python app.py

# Linux/Mac
export FLASK_ENV=development
python app.py
```

### Database Management
```bash
# Access MySQL
mysql -u root -p

# Use database
USE iserbisyo_db;

# View tables
SHOW TABLES;

# Backup database
mysqldump -u root iserbisyo_db > backup.sql

# Restore database
mysql -u root iserbisyo_db < backup.sql
```

### Common Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Upgrade dependencies
pip install --upgrade -r requirements.txt

# Freeze dependencies
pip freeze > requirements.txt

# Run with custom host/port
python app.py --host=0.0.0.0 --port=8000
```

---

## 🚀 Production Deployment

### 1. Prepare Application
```bash
# Set production environment
export FLASK_ENV=production

# Update secret key
export SECRET_KEY="generate-strong-random-key"

# Configure production database
export DATABASE_URL="mysql://user:password@host/database"
```

### 2. Use Production Server (Gunicorn)
```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Run with Gevent workers (better for I/O)
pip install gevent
gunicorn -k gevent -w 4 -b 0.0.0.0:8000 app:app
```

### 3. Configure Nginx (Reverse Proxy)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/new-iserbisyo/static;
    }
}
```

### 4. SSL Certificate (Let's Encrypt)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## 📦 Dependencies

### Core Dependencies
- **Flask** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **PyMySQL** - MySQL connector
- **Werkzeug** - Security utilities
- **python-dotenv** - Environment configuration
- **Jinja2** - Template engine
- **SQLAlchemy** - SQL toolkit

### Optional Dependencies
- **Flask-Mail** - Email support
- **python-dateutil** - Date utilities
- **Gunicorn** - Production WSGI server
- **Gevent** - Async worker

---

## 🐛 Troubleshooting

### Database Connection Issues
```python
# Check MySQL is running
# In XAMPP, start MySQL service

# Verify database exists
mysql -u root -e "SHOW DATABASES;"

# Check connection string
# config.py: mysql://root:@localhost/iserbisyo_db
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version  # Should be 3.8+
```

### Session Issues
```python
# Clear browser cookies
# Check SECRET_KEY is set
# Verify session configuration in config.py
```

### File Upload Issues
```bash
# Check upload directory exists
mkdir -p static/uploads/profiles
mkdir -p static/uploads/documents

# Verify permissions
chmod 755 static/uploads
```

---

## 📝 API Endpoints

### Admin API
- `POST /admin/api/resident/<id>/approve` - Approve resident
- `POST /admin/api/resident/<id>/reject` - Reject resident
- `GET /admin/api/users` - Get all users
- `POST /admin/api/certificate/<id>/update-status` - Update certificate status

### Clerk API
- `GET /clerk/api/users` - Get users (admin/clerk only)
- `GET /clerk/api/certificate` - Get certificate details
- `POST /clerk/api/certificate/<id>/proceed-payment` - Move to payment

### Resident API
- `POST /resident/certificate/request` - Submit certificate request
- `POST /resident/certificate/<id>/edit` - Edit pending request
- `POST /resident/certificate/<id>/cancel` - Cancel request

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Write docstrings for functions
- Keep functions small and focused

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Contact: support@iserbisyo.com
- Documentation: [GitHub Wiki](link-to-wiki)

---

## 🎉 Acknowledgments

- Flask community for excellent documentation
- Tailwind CSS for the utility-first CSS framework
- Font Awesome for beautiful icons
- All contributors and testers

---

## 📈 Roadmap

### Upcoming Features
- [ ] Email notifications for certificate status
- [ ] SMS notifications integration
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Document scanning integration
- [ ] QR code certificate verification
- [ ] Multi-language support
- [ ] API documentation (Swagger)
- [ ] Automated backup system
- [ ] Data export (Excel, PDF)

---

**Made with ❤️ for Philippine Barangays**

---

**Version:** 1.0.0  
**Last Updated:** October 2025  
**Status:** Production Ready ✅
