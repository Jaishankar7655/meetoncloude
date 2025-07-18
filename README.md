# Meeting on Cloud - Django Web Application

A comprehensive Django-based web application for managing virtual classrooms and meetings with user authentication, OTP verification, and classroom management features.

## Features

### 🔐 Authentication System
- **User Registration** with email OTP verification
- **Secure Login** with session management
- **Remember Me** functionality
- **Profile Management** with image uploads
- **Password-based Authentication**

### 🏫 Classroom Management
- **Create Classrooms** with custom details
- **Search Classrooms** by teacher name or class code
- **Class Code System** for easy classroom identification
- **Resource Management** for classroom materials
- **Teacher Dashboard** for managing multiple classrooms

### 📧 Email Integration
- **OTP Verification** via email for registration
- **Resend OTP** functionality
- **HTML Email Templates** for professional communication

### 💻 Modern Architecture
- **Docker Containerization** for easy deployment
- **Nginx Reverse Proxy** for production-ready setup
- **MySQL Database** with persistent data storage
- **Multi-stage Docker Build** for optimized images

## Technology Stack

- **Backend**: Django 4.x (Python)
- **Database**: MySQL 8.0
- **Web Server**: Nginx
- **Application Server**: Gunicorn
- **Containerization**: Docker & Docker Compose
- **Email**: Django Email Framework
- **Frontend**: HTML, CSS, JavaScript (Django Templates)

## Prerequisites

- Docker and Docker Compose installed
- Python 3.12+ (for local development)
- MySQL 8.0+ (for local development)
- SMTP email service credentials

## Quick Start with Docker

### 1. Clone the Repository
```bash
git clone <repository-url>
cd meeting-on-cloud
```

### 2. Environment Configuration
Create a `.env` file in the project root:
```env
# Database Configuration
DB_NAME=book
DB_USER=appuser
DB_PASSWORD=apppass
DB_HOST=mysql
DB_PORT=3306

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

### 3. Build and Run with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d --build
```

### 4. Access the Application
- **Application**: http://localhost
- **Admin Panel**: http://localhost/admin
--**on server** :http://3.6.93.201/userLogin/
- **Database**: localhost:3306

## Local Development Setup

### 1. Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Create database
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

## Project Structure

```
meeting-on-cloud/
├── meetingoncloude/          # Main Django project
├── meet/                     # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Django forms
│   ├── urls.py              # URL patterns
│   └── templates/           # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
├── nginx/                   # Nginx configuration
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml       # Docker services configuration
├── Dockerfile              # Django application container
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables
```

## API Endpoints

### Authentication
- `POST /register/` - User registration
- `POST /login/` - User login
- `POST /logout/` - User logout
- `POST /otp-verify/` - OTP verification
- `POST /resend-otp/` - Resend OTP

### Classroom Management
- `GET /dashboard/` - User dashboard
- `POST /create-classroom/` - Create new classroom
- `GET /search-class/` - Search classrooms
- `GET /my-resources/` - User's created classrooms
- `GET /class-code/` - View class codes
- `GET /my-material/` - View classroom materials

## Models

### UserRegister
- User authentication and profile management
- Auto-generated 6-digit class codes
- Profile image uploads

### Create_classroom
- Classroom creation and management
- Teacher information storage
- File upload capabilities

### join_classroom
- Classroom membership tracking
- User-classroom relationships

## Docker Services

### Django Application
- **Image**: Python 3.12-slim with multi-stage build
- **Port**: 8000
- **Server**: Gunicorn WSGI server
- **Auto-migration**: Runs migrations on startup

### MySQL Database
- **Image**: MySQL 8.0
- **Port**: 3306
- **Persistent Storage**: Docker volume for data persistence
- **Default Database**: `book`

### Nginx Reverse Proxy
- **Port**: 80
- **Load Balancing**: Upstream to Django application
- **Static Files**: Efficient serving of static and media files
- **SSL Ready**: Easy HTTPS configuration

## Email Configuration

The application uses Django's email framework for OTP verification:

```python
# Gmail Configuration Example
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-specific-password'
```

## Security Features

- **Session Management**: Secure session handling
- **OTP Verification**: Email-based account verification
- **Password Protection**: Secure password storage
- **File Upload Security**: Secure file handling
- **CSRF Protection**: Django's built-in CSRF protection

## Production Deployment

### Docker Compose Production
```bash
# Production build
docker-compose -f docker-compose.prod.yml up --build -d

# View logs
docker-compose logs -f django
```

### Manual Deployment
1. Set `DEBUG=False` in settings
2. Configure proper `ALLOWED_HOSTS`
3. Set up SSL certificates
4. Configure static file serving
5. Set up database backups

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check if MySQL container is running
docker-compose ps

# View database logs
docker-compose logs mysql
```

**Email Sending Failed**
- Verify SMTP credentials in `.env`
- Check if less secure apps are enabled (Gmail)
- Use app-specific passwords for Gmail

**Static Files Not Loading**
```bash
# Collect static files
python manage.py collectstatic

# Check Nginx configuration
docker-compose logs nginx
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## Acknowledgments

- Django framework for robust web development
- Docker for containerization
- MySQL for reliable data storage
- Nginx for high-performance web serving