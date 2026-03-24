# Doctor Search System - Complete Django Application

A production-ready Django web application for searching doctors, booking appointments, reading reviews, and managing user profiles with a REST API.

## 🌟 Features

### User Features
- 👤 User Registration & Authentication
- 🔍 Live Search with AJAX (name, location, experience)
- 📅 Book Appointments
- ⭐ Write & Read Reviews
- 👥 User Profile Management
- 📱 Fully Responsive Design
- 🎨 Modern UI with Gradient

### Doctor Features
- 📊 Doctor Profiles with Ratings
- 🏥 Multi-specialization Support
- 📍 Location-based Search
- 💼 Professional Experience Display
- ✍️ Review Management

### API Features
- 🔐 Token-based Authentication
- 📡 RESTful Endpoints
- 📄 Pagination & Filtering
- ⚡ Rate Limiting
- 📝 Comprehensive API Documentation

### Admin Features
- 👨‍💼 Doctor Management
- 📋 Appointment Management
- ⭐ Review Moderation
- 👥 User Management

## 📋 Requirements

- Python 3.8+
- Django 6.0.3
- Django REST Framework 3.17.0
- django-filter 25.2
- SQLite or PostgreSQL

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
# Navigate to project directory
cd doctor_search

# Create virtual environment
python -m venv myvenv

# Activate virtual environment
# On Windows:
myvenv\Scripts\activate
# On macOS/Linux:
source myvenv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

```bash
cd doctor_search

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (for admin access)
python manage.py createsuperuser
# Enter: username, email, password
```

### 4. Create Sample Data

```bash
python manage.py shell

# Inside shell, create doctors:
from doctors.models import Doctor

Doctor.objects.create(
    name="Dr. John Smith",
    specialization="Cardiology",
    location="New York",
    experience=10,
    contact="555-1234",
    email="john@example.com",
    qualification="MD, Harvard Medical School",
    clinic_name="Smith Cardiology Clinic"
)

Doctor.objects.create(
    name="Dr. Sarah Johnson",
    specialization="Dermatology",
    location="Los Angeles",
    experience=8,
    contact="555-5678",
    email="sarah@example.com",
    qualification="MD, Yale School of Medicine",
    clinic_name="Johnson Dermatology Center"
)

exit()
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit http://localhost:8000/ in your browser.

## 📚 Project Structure

```
doctor_search/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── doctor_search/                     # Project configuration
│   ├── settings.py                   # Django settings
│   ├── urls.py                       # Main URL configuration
│   ├── wsgi.py                       # Production WSGI app
│   └── asgi.py                       # ASGI configuration
└── doctors/                           # Main Django app
    ├── models.py                     # Database models (Doctor, Appointment, Review, UserProfile)
    ├── views.py                      # Web views
    ├── api_views.py                  # REST API views
    ├── serializers.py                # DRF serializers
    ├── forms.py                      # Django forms (Registration, Login, Profile, etc.)
    ├── admin.py                      # Admin configuration
    ├── signals.py                    # Django signals (User profile creation, Token generation)
    ├── urls.py                       # App URL patterns
    ├── api_urls.py                   # API URL patterns
    ├── static/
    │   └── js/
    │       └── live_search.js        # AJAX live search implementation
    └── templates/
        ├── search.html               # Main search page (with live search)
        ├── book_appointment.html     # Appointment booking form
        └── confirmation.html         # Appointment confirmation page
```

## 🛣️ Available URLs

### Web Interface
- `http://localhost:8000/` - Home (Search page)
- `http://localhost:8000/book/` - Book Appointment
- `http://localhost:8000/book/<doctor_id>/` - Book for Specific Doctor
- `http://localhost:8000/admin/` - Admin Panel

### REST API
- `http://localhost:8000/api/` - API Root
- `http://localhost:8000/api/doctors/` - List Doctors
- `http://localhost:8000/api/doctors/search/?name=...&location=...&min_experience=...` - Search
- `http://localhost:8000/api/appointments/` - User Appointments
- `http://localhost:8000/api/reviews/` - Reviews
- `http://localhost:8000/api/register/` - Register User
- `http://localhost:8000/api/auth-token/` - Get Authentication Token

## 🔑 API Authentication

### Get Authentication Token

```bash
curl -X POST http://localhost:8000/api/auth-token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"youruser","password":"yourpass"}'
```

### Use Token in Requests

```bash
curl http://localhost:8000/api/doctors/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## 📖 Main Features Explained

### 1. Live Search with AJAX
- Type in search fields (name, location, experience)
- Results update in real-time without page reload
- Uses Fetch API to call Django REST endpoints
- Animated loading spinner shows during search
- File: `doctors/static/js/live_search.js`

### 2. User Authentication
- Registration form with password validation
- Login with username/password
- Session-based authentication for web
- Token-based authentication for API
- Automatic UserProfile creation on signup

### 3. Appointment Booking
- Select doctor and date
- Optional time and notes
- Status tracking (pending, confirmed, completed, cancelled)
- Only logged-in users can book

### 4. Reviews & Ratings
- Leave reviews with 1-5 star rating
- View average doctor rating
- One review per user per doctor
- Mark reviews as helpful

### 5. User Profile
- Extended user profile with bio, phone, address
- Automatic creation on user registration
- Editable through API and admin panel

## 🔐 Security Features

- ✅ Password Hashing (PBKDF2)
- ✅ CSRF Protection
- ✅ SQL Injection Prevention (ORM)
- ✅ XSS Protection (Template Escaping, HTML Escaping in API)
- ✅ Rate Limiting (100/hour anonymous, 1000/hour authenticated)
- ✅ Token-based API Authentication
- ✅ Session Security
- ✅ Permission-based Access Control

## 🗄️ Database Models

### Doctor
- name, specialization, location, experience, contact, email
- bio, qualification, clinic_name
- average_rating (0-5), total_reviews
- timestamps (created_at, updated_at)

### Appointment
- patient (ForeignKey to User)
- doctor (ForeignKey to Doctor)
- date, time, status (pending/confirmed/completed/cancelled)
- notes, timestamps

### Review
- doctor, user, rating (1-5), title, comment
- helpful_count
- timestamps
- Unique: one review per user per doctor

### UserProfile (Extended User)
- bio, phone, date_of_birth
- address, city, state
- timestamps

## 💡 Usage Examples

### Register New User (API)

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepass123",
    "password2": "securepass123"
  }'
```

### Search Doctors (API)

```bash
# Search by name and minimum experience
curl "http://localhost:8000/api/doctors/search/?name=John&min_experience=5"

# Filter by specialization
curl "http://localhost:8000/api/doctors/search/?specialization=Cardiology"

# Filter by location
curl "http://localhost:8000/api/doctors/search/?location=New%20York"

# Combined search
curl "http://localhost:8000/api/doctors/search/?name=Smith&location=New%20York&min_experience=8"
```

### Get Doctor Details with Reviews

```bash
curl http://localhost:8000/api/doctors/1/
```

### Book Appointment (API)

```bash
curl -X POST http://localhost:8000/api/appointments/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor": 1,
    "date": "2024-04-15",
    "time": "14:30",
    "notes": "Have a chronic headache"
  }'
```

### Write Review (API)

```bash
curl -X POST http://localhost:8000/api/reviews/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor": 1,
    "rating": 5,
    "title": "Excellent doctor",
    "comment": "Very professional and caring"
  }'
```

## 🧪 Testing the Application

### Manual Testing Checklist

```
[ ] User Registration - Complete
[ ] User Login - Complete
[ ] Live Search (AJAX) - Complete
  [ ] Search by name
  [ ] Search by location
  [ ] Filter by experience
  [ ] No results message displays correctly
[ ] Doctor Details - Complete
[ ] Appointment Booking - Complete
  [ ] Can select doctor
  [ ] Can select date
  [ ] Cannot select past dates
  [ ] Success confirmation
[ ] Reviews - Complete
  [ ] Can write review
  [ ] Can read reviews
  [ ] Rating displays correctly
[ ] API Endpoints - Complete
  [ ] GET /api/doctors/
  [ ] POST /api/register/
  [ ] GET /api/appointments/ (authenticated)
  [ ] POST /api/reviews/ (authenticated)
```

## 📝 Admin Access

1. Go to `http://localhost:8000/admin/`
2. Login with superuser credentials
3. Manage:
   - Doctors (add, edit, delete)
   - Appointments (view, modify status)
   - Reviews (moderate, delete)
   - Users (manage profiles)

## 🚀 Deploy to Production

### Option 1: Heroku

```bash
# Install Heroku CLI

# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

### Option 2: PythonAnywhere

1. Upload code to PythonAnywhere
2. Create virtual environment
3. Install dependencies
4. Configure web app settings
5. Run migrations

### Option 3: DigitalOcean/AWS/Linode

See [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) for detailed deployment instructions.

## 📚 Documentation Files

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete REST API Reference
- **[LIVE_SEARCH_GUIDE.md](LIVE_SEARCH_GUIDE.md)** - Live Search Implementation Details
- **[PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md)** - Production Deployment Guide

## 🐛 Common Issues & Solutions

### Issue: Static files not loading (404)

```bash
python manage.py collectstatic
```

### Issue: Database migration errors

```bash
python manage.py makemigrations
python manage.py migrate --fake-initial
```

### Issue: Permission denied on API endpoints

Ensure you're including the authentication token:
```bash
-H "Authorization: Token YOUR_TOKEN"
```

### Issue: CORS errors in API

Add django-cors-headers:
```bash
pip install django-cors-headers
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 💬 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Contact the development team

## 🎉 Thank You

Thank you for using Doctor Search System! We hope this helps connect patients with the right doctors.

---

**Last Updated:** 2024
**Version:** 1.0.0
**Status:** Production Ready
