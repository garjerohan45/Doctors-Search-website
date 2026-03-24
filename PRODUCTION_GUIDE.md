# Doctor Search System - Production Deployment Guide

## Project Overview

This is a production-ready Django application for searching doctors, booking appointments, and managing reviews. It includes a REST API with authentication, a responsive web interface, and comprehensive user management.

## Technology Stack

- **Backend:** Django 6.0.3
- **API:** Django REST Framework 3.17.0
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **Frontend:** HTML/CSS/JavaScript (Vanilla JS)
- **Authentication:** Token-based & Session-based

## Project Structure

```
doctor_search/
├── doctor_search/          # Project settings
│   ├── settings.py        # Django configuration
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI application
│   └── asgi.py            # ASGI application
├── doctors/                # Main application
│   ├── models.py          # Database models
│   ├── views.py           # Web views
│   ├── api_views.py       # REST API views
│   ├── serializers.py     # DRF serializers
│   ├── forms.py           # Django forms
│   ├── admin.py           # Django admin configuration
│   ├── signals.py         # Signal handlers
│   ├── urls.py            # App URLs
│   ├── api_urls.py        # API URLs
│   ├── static/            # Static files
│   │   └── js/
│   │       └── live_search.js
│   └── templates/         # HTML templates
│       ├── search.html
│       ├── book_appointment.html
│       └── confirmation.html
├── manage.py              # Django management
├── requirements.txt       # Python dependencies
└── db.sqlite3            # Database (Development)
```

## Database Models

### 1. Doctor Model
```python
- name (CharField)
- specialization (CharField, with choices)
- location (CharField)
- experience (IntegerField)
- contact (CharField)
- email (EmailField, unique)
- bio (TextField, optional)
- qualification (CharField, optional)
- clinic_name (CharField, optional)
- average_rating (FloatField, 0-5)
- total_reviews (IntegerField)
- created_at (DateTimeField, auto)
- updated_at (DateTimeField, auto)
```

### 2. User Model (Extended from Django User)
- First Name, Last Name, Email
- Username, Password

### 3. UserProfile Model
```python
- user (OneToOneField to User)
- bio (TextField, optional)
- phone (CharField, optional)
- date_of_birth (DateField, optional)
- address (CharField, optional)
- city (CharField, optional)
- state (CharField, optional)
- created_at (DateTimeField, auto)
- updated_at (DateTimeField, auto)
```

### 4. Appointment Model
```python
- patient (ForeignKey to User)
- doctor (ForeignKey to Doctor)
- date (DateField)
- time (TimeField, optional)
- status (CharField, choices: pending/confirmed/completed/cancelled)
- notes (TextField, optional)
- created_at (DateTimeField, auto)
- updated_at (DateTimeField, auto)
```

### 5. Review Model
```python
- doctor (ForeignKey to Doctor)
- user (ForeignKey to User)
- rating (IntegerField, 1-5)
- title (CharField)
- comment (TextField)
- created_at (DateTimeField, auto)
- updated_at (DateTimeField, auto)
- helpful_count (IntegerField)
- unique_together: (doctor, user)  # One review per user per doctor
```

## Setup Instructions

### 1. Clone and Install

```bash
# Clone the repository
git clone <repo-url>
cd doctor_search

# Create virtual environment
python -m venv myvenv

# Activate virtual environment
# On Windows:
myvenv\Scripts\activate
# On macOS/Linux:
source myvenv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Database

```bash
# Create migrations for new models
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

### 4. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000/` in your browser.

## API Endpoints

### Authentication
- **POST** `/api/register/` - Register new user
- **POST** `/api/auth-token/` - Get authentication token

### Doctors
- **GET** `/api/doctors/` - List all doctors
- **POST** `/api/doctors/` - Create doctor (admin only)
- **GET** `/api/doctors/<id>/` - Get doctor details
- **PUT** `/api/doctors/<id>/` - Update doctor (admin)
- **DELETE** `/api/doctors/<id>/` - Delete doctor (admin)
- **GET** `/api/doctors/search/?name=...&location=...&min_experience=...` - Search doctors
- **GET** `/api/doctors/<id>/reviews/` - Get doctor reviews
- **GET** `/api/doctors/<id>/appointments/` - Get appointment count

### Appointments
- **GET** `/api/appointments/` - List user's appointments
- **POST** `/api/appointments/` - Create appointment
- **GET** `/api/appointments/<id>/` - Get appointment details
- **PUT** `/api/appointments/<id>/` - Update appointment
- **DELETE** `/api/appointments/<id>/` - Cancel appointment

### Reviews
- **GET** `/api/reviews/` - List reviews
- **POST** `/api/reviews/` - Create review (authenticated)
- **GET** `/api/reviews/<id>/` - Get review
- **PUT** `/api/reviews/<id>/` - Update review (own review)
- **DELETE** `/api/reviews/<id>/` - Delete review (own review)
- **POST** `/api/reviews/<id>/mark_helpful/` - Mark review as helpful

### User Profile
- **GET** `/api/profile/me/` - Get current user profile
- **PUT** `/api/profile/me/` - Update profile
- **PATCH** `/api/profile/me/` - Partially update profile

## Authentication

### Token Authentication (Recommended for API)

1. Register: `POST /api/register/`
2. Get Token: `POST /api/auth-token/`
3. Use Token in Headers:
   ```bash
   Authorization: Token <your-token>
   ```

### Session Authentication
- Login through web interface
- Session cookie maintained

## Features

### User Features
- ✅ User Registration & Login
- ✅ Search doctors by name, location, experience
- ✅ Book appointments
- ✅ View appointment history
- ✅ Write and read reviews
- ✅ Update user profile
- ✅ Live search with AJAX

### Admin Features
- ✅ Manage doctors
- ✅ Manage appointments
- ✅ Moderate reviews
- ✅ View user profiles

### API Features
- ✅ RESTful endpoints
- ✅ Token-based authentication
- ✅ Pagination (10 items per page)
- ✅ Filtering & Searching
- ✅ Rate limiting (100/hour anonymous, 1000/hour authenticated)

## Security Features

### Implemented
- ✅ Password hashing (PBKDF2)
- ✅ Token authentication
- ✅ CSRF protection
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection (template escaping)
- ✅ Rate limiting
- ✅ Session security
- ✅ User permissions (IsAuthenticated, IsAuthenticatedOrReadOnly)

### Production Checklist

Before deploying to production:

1. **Security Settings**
   ```python
   DEBUG = False
   SECRET_KEY = <generate-new-secret-key>
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   SECURE_HSTS_SECONDS = 31536000
   ```

2. **Database**
   - Use PostgreSQL (not SQLite)
   - Enable backups
   - Use strong passwords

3. **Static Files**
   - Serve via CDN (CloudFront, Cloudflare)
   - Configure whitenoise middleware

4. **Environment Variables**
   ```bash
   SECRET_KEY=your-secret-key
   DEBUG=False
   DATABASE_URL=postgresql://...
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

5. **Logging & Monitoring**
   - Configure error logging
   - Set up application monitoring
   - Monitor API rate limits

6. **Email Configuration**
   - Configure SMTP for appointment confirmations
   - Set up password reset emails

7. **Deployment**
   - Use Gunicorn/uWSGI for app server
   - Use Nginx as reverse proxy
   - Use Docker for containerization
   - Use CI/CD pipeline (GitHub Actions)

## Testing

### Run Tests
```bash
python manage.py test
```

### Test API Endpoints
```bash
# Create test data
python manage.py shell

# Register user
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username":"testuser",
    "email":"test@example.com",
    "password":"testpass123",
    "password2":"testpass123"
  }'

# Get token
curl -X POST http://localhost:8000/api/auth-token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Use token
curl http://localhost:8000/api/doctors/ \
  -H "Authorization: Token <token>"
```

## Performance Optimization

### Database
- Use select_related() for ForeignKeys
- Use prefetch_related() for reverse relations
- Add database indexes on frequently queried fields
- Use Celery for background tasks

### Caching
- Implement Redis caching
- Cache doctor list (invalidate on updates)
- Cache user profiles

### API
- Implement pagination (done)
- Use gzip compression
- Implement query optimization
- Use async tasks for email notifications

## Monitoring & Maintenance

### Health Checks
- Monitor API response times
- Monitor database performance
- Monitor error rates

### Maintenance Tasks
- Regular database backups
- Monitor error logs
- Update dependencies
- Review user activity

## Deployment Options

### 1. Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### 2. AWS EC2
- Launch EC2 instance
- Install Python, PostgreSQL
- Clone repository
- Configure Gunicorn + Nginx
- Configure domain with Route53

### 3. Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn doctor_search.wsgi:application --bind 0.0.0.0:8000
```

### 4. DigitalOcean
- Create Droplet
- Install dependencies
- Deploy with App Platform

## Documentation

- API Documentation: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- Live Search Guide: [LIVE_SEARCH_GUIDE.md](LIVE_SEARCH_GUIDE.md)

## Troubleshooting

### Common Issues

**Issue:** 404 errors on admin interface
```bash
python manage.py collectstatic
```

**Issue:** Database migration errors
```bash
python manage.py makemigrations
python manage.py migrate --fake-initial
```

**Issue:** Authentication errors on API
- Ensure token is in Authorization header
- Format: `Authorization: Token <token>`

**Issue:** CORS errors
- Add appropriate CORS headers
- Use django-cors-headers package

## Contributing

1. Fork repository
2. Create feature branch
3. Write tests
4. Submit pull request

## License

MIT License - See LICENSE file

## Support

For issues and questions:
- Report bugs via GitHub Issues
- Check documentation
- Contact: support@doctorsearch.com
