# Doctor Search System - Quick Reference Guide

> This document provides quick access to key information for developers working with the system.

---

## 📁 Project Structure

```
doctor_search/
├── manage.py                 # Django management CLI
├── db.sqlite3               # Development database
├── requirements.txt         # Python dependencies
├── setup.sh                 # Automated setup script
│
├── doctor_search/           # Main project configuration
│   ├── __init__.py
│   ├── settings.py          # Django settings, REST_FRAMEWORK config
│   ├── urls.py              # Main URL router
│   ├── asgi.py              # ASGI config (production)
│   └── wsgi.py              # WSGI config (production)
│
├── doctors/                 # Main application
│   ├── models.py            # Doctor, Appointment, Review, UserProfile
│   ├── views.py             # Web views (search page)
│   ├── api_views.py         # REST API viewsets (5 services)
│   ├── api_urls.py          # API routing
│   ├── serializers.py       # API serialization (7 serializers)
│   ├── forms.py             # Django forms (5 forms)
│   ├── admin.py             # Django admin configuration
│   ├── signals.py           # Signal handlers (auto profile/token)
│   ├── urls.py              # Web routing
│   ├── apps.py              # App config with signal imports
│   ├── migrations/          # Database migrations
│   ├── templates/           # HTML templates
│   │   └── search.html      # Main search page
│   └── static/
│       └── js/
│           └── live_search.js  # AJAX live search implementation
│
├── myvenv/                  # Virtual environment
│
└── DOCUMENTATION FILES:
    ├── README.md             # Getting started guide
    ├── PRODUCTION_GUIDE.md   # Deployment guide
    ├── API_DOCUMENTATION.md  # API reference
    ├── LIVE_SEARCH_GUIDE.md  # Frontend implementation
    └── ARCHITECTURE.md       # This file (System design)
```

---

## 🗂️ File Reference Quick Access

| File | Purpose | Key Content |
|------|---------|------------|
| [doctors/models.py](doctors/models.py) | Data models | 5 models, relationships, validators |
| [doctors/serializers.py](doctors/serializers.py) | API serialization | 7 serializers for all endpoints |
| [doctors/api_views.py](doctors/api_views.py) | API logic | 5 viewsets with custom actions |
| [doctors/forms.py](doctors/forms.py) | Web forms | 5 forms with validation |
| [doctors/admin.py](doctors/admin.py) | Admin interface | Rich admin config with filters |
| [doctors/signals.py](doctors/signals.py) | Signal handlers | Auto profile & token creation |
| [doctor_search/settings.py](doctor_search/settings.py) | Configuration | REST_FRAMEWORK, apps config |
| [doctors/static/js/live_search.js](doctors/static/js/live_search.js) | Frontend | AJAX search, debouncing |

---

## 🔍 Quick Command Reference

### Initial Setup
```bash
# Activate virtual environment
myvenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create sample data (optional)
python manage.py shell
# Inside shell:
from doctors.models import Doctor
Doctor.objects.create(
    name="Dr. John Smith",
    specialization="Cardiology",
    location="New York",
    experience=10,
    contact="555-1234",
    email="john@example.com"
)

# Run development server
python manage.py runserver

# Access points:
# - Web: http://localhost:8000/
# - Admin: http://localhost:8000/admin/
# - API Root: http://localhost:8000/api/
```

### API Testing
```bash
# Register new user
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password2": "securepass123"
  }'

# Get authentication token
curl -X POST http://localhost:8000/api/auth-token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'

# Search doctors (no auth required)
curl http://localhost:8000/api/doctors/search/?name=John&specialization=Cardiology

# List user's appointments (requires token)
curl http://localhost:8000/api/appointments/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"

# Create appointment
curl -X POST http://localhost:8000/api/appointments/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor": 1,
    "date": "2024-04-15",
    "time": "14:30"
  }'

# Create review
curl -X POST http://localhost:8000/api/reviews/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor": 1,
    "rating": 5,
    "title": "Excellent",
    "comment": "Very professional"
  }'
```

---

## 📊 Data Model Overview

### Model Relationships
```
User (Django)
  ├─ 1:1 ← UserProfile (auto-created)
  ├─ 1:1 ← Token (auto-created)
  ├─ 1:* → Appointment (as patient)
  └─ 1:* → Review (as author)

Doctor
  ├─ *:1 ← Appointment (has many)
  └─ *:1 ← Review (has many)
```

### Model Fields Reference

**Doctor**
- `name` - CharField(100)
- `specialization` - CharField(choices)
- `location` - CharField(100)
- `experience` - IntegerField(≥0, validated)
- `contact` - CharField(15)
- `email` - EmailField(unique)
- `bio`, `qualification`, `clinic_name` - Optional text fields
- `average_rating` - FloatField(0-5, calculated)
- `total_reviews` - IntegerField(≥0, calculated)
- Timestamps: `created_at`, `updated_at`

**Appointment**
- `patient` - ForeignKey(User, CASCADE)
- `doctor` - ForeignKey(Doctor, CASCADE)
- `date` - DateField (validated: not past)
- `time` - TimeField (optional)
- `status` - CharField(choices: pending/confirmed/completed/cancelled)
- `notes` - TextField (optional)
- Timestamps: `created_at`, `updated_at`

**Review**
- `doctor` - ForeignKey(Doctor, CASCADE)
- `user` - ForeignKey(User, CASCADE)
- `rating` - IntegerField(1-5, choices)
- `title` - CharField(200)
- `comment` - TextField
- `helpful_count` - IntegerField
- Constraint: unique_together(doctor, user)
- Timestamps: `created_at`, `updated_at`

**UserProfile**
- `user` - OneToOneField(User, CASCADE)
- `bio` - TextField (optional)
- `phone` - CharField(15, optional)
- `date_of_birth` - DateField (optional)
- `address` - CharField(255, optional)
- `city`, `state` - CharField (optional)
- Timestamps: `created_at`, `updated_at`

---

## 🔐 Authentication & Authorization

### Token Generation Flow
```
1. User registers at /api/register/
   ↓
2. Signal creates UserProfile + Token
   ↓
3. User retrieves token at /api/auth-token/
   ↓
4. User includes token in requests:
   Header: Authorization: Token {token}
   ↓
5. TokenAuthentication class validates
   ↓
6. View-level permissions checked
```

### Permission Classes

| Class | Usage | Access |
|-------|-------|--------|
| `AllowAny` | Public endpoints | Everyone |
| `IsAuthenticated` | Protected endpoints | Logged-in users only |
| `IsAuthenticatedOrReadOnly` | Mixed endpoints | Read: all, Write: auth only |

### API Endpoints & Permissions

| Endpoint | Method | Permission | Purpose |
|----------|--------|-----------|---------|
| `/api/register/` | POST | AllowAny | User registration |
| `/api/auth-token/` | POST | AllowAny | Get auth token |
| `/api/doctors/` | GET | AllowAny | List all doctors |
| `/api/doctors/search/` | GET | AllowAny | Search doctors |
| `/api/doctors/{id}/` | GET | AllowAny | Doctor detail |
| `/api/appointments/` | GET | IsAuthenticated | List own appointments |
| `/api/appointments/` | POST | IsAuthenticated | Create appointment |
| `/api/reviews/` | POST | IsAuthenticated | Create review |
| `/api/reviews/` | GET | AllowAny | List reviews |
| `/api/profile/me/` | GET/PUT/PATCH | IsAuthenticated | Own profile |

---

## 🔄 Key Workflows

### Registration & Login
```
1. User POST /api/register/ with username/email/password
2. Serializer validates:
   - Passwords match
   - Username unique
   - Email unique
3. User created with hashed password (PBKDF2)
4. Signal post_save triggered:
   - UserProfile created
   - Token created
5. Response with user data (200 Created)
```

### Doctor Search
```
1. User GET /api/doctors/search/?name=john&specialization=cardiology
2. View applies filters:
   - name__icontains=john
   - specialization__icontains=cardiology
3. Ordered by: -average_rating, name
4. Paginated: 10 results per page
5. Serialized and returned (200 OK)
```

### Appointment Booking
```
1. Authenticated user POST /api/appointments/
   {doctor: 1, date: "2024-04-15", time: "14:30"}
2. Validation checks:
   - User is authenticated
   - Date not in past
3. Appointment created with:
   - patient = current user
   - status = "pending"
4. Signal could send email notification
5. Response with appointment details (201 Created)
```

### Review & Rating System
```
1. Authenticated user POST /api/reviews/
   {doctor: 1, rating: 5, title: "...", comment: "..."}
2. Validation checks:
   - One review per user per doctor (unique_together)
   - Rating 1-5 valid
3. Review created with user auto-set
4. Signal update_doctor_rating() recalculates:
   - average_rating = sum(ratings) / count
   - total_reviews = count
5. Doctor model updated automatically
6. Response with review details (201 Created)
```

### Live Search (Frontend)
```
1. User types in search box
2. Input event fires
3. Debounce wait 500ms (no more typing)
4. Fetch /api/doctors/search/?name=typed_text
5. Show loading spinner
6. Process JSON response
7. Generate HTML cards for each result
8. Inject into DOM
9. Hide spinner
```

---

## 🛠️ Common Development Tasks

### Add New Doctor Specialization
1. Edit `doctors/models.py`
2. Add choice to `SPECIALIZATION_CHOICES`
3. Run `python manage.py makemigrations`
4. Run `python manage.py migrate`

### Add New API Field
1. Add field to model in `doctors/models.py`
2. Add field to serializer in `doctors/serializers.py`
3. Create migration: `python manage.py makemigrations`
4. Apply migration: `python manage.py migrate`

### Add New API Endpoint
1. Create method in appropriate ViewSet in `doctors/api_views.py`
2. Use `@action(detail=False, methods=['get'])` decorator
3. Router automatically registers it
4. Access at `/api/{viewset}/{action}/`

### Change Pagination Size
1. Edit `doctor_search/settings.py`
2. Update `REST_FRAMEWORK['PAGE_SIZE']`
3. Restart server

### Update Rate Limiting
1. Edit `doctor_search/settings.py`
2. Change `DEFAULT_THROTTLE_RATES`
3. Restart server

---

## 🐛 Debugging Tips

### Check Database State
```bash
python manage.py shell
>>> from doctors.models import Doctor, Review
>>> Doctor.objects.all()  # List all doctors
>>> Doctor.objects.filter(specialization='Cardiology')
>>> doctor = Doctor.objects.first()
>>> doctor.average_rating  # Check calculated rating
>>> doctor.reviews.all()   # See all reviews
```

### View API Response Details
```bash
# Install django-extensions for better shell
pip install django-extensions

# Use ipython
python manage.py shell_plus

# Test query manually
from doctors.models import Doctor
from doctors.serializers import DoctorSerializer
doctor = Doctor.objects.first()
serializer = DoctorSerializer(doctor)
print(serializer.data)  # See exact JSON output
```

### Check Running Processes
```bash
# Find process on port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Mac/Linux

# Kill process
taskkill /PID {pid} /F        # Windows
kill -9 {pid}                 # Mac/Linux
```

### Database Migration Issues
```bash
# Show migration history
python manage.py showmigrations

# View SQL for migration
python manage.py sqlmigrate doctors 0001_initial

# Rollback migration
python manage.py migrate doctors 0001  # Go back to this migration

# Clear all migrations (dev only!)
python manage.py migrate doctors zero
```

---

## 📈 Performance Metrics & Targets

| Metric | Target | How to Monitor |
|--------|--------|----------------|
| API Response Time | < 200ms | Django Debug Toolbar |
| Error Rate | < 0.1% | Error logs |
| Database Query Time | < 100ms | django-extensions |
| Page Load Time | < 1s | Browser DevTools |
| API Throughput | >1000 req/min | Load testing |

---

## 🚀 Deployment Checklist

- [ ] Set `DEBUG = False` in settings.py
- [ ] Generate new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up HTTPS/SSL
- [ ] Configure email backend (Gmail/SendGrid)
- [ ] Switch to PostgreSQL database
- [ ] Run migrations on production: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Configure environment variables
- [ ] Test all API endpoints
- [ ] Set up error tracking (Sentry)
- [ ] Configure monitoring
- [ ] Set up backups
- [ ] Test disaster recovery

---

## 📞 Support Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Django Filter**: https://django-filter.readthedocs.io/

## 📋 See Also

- [README.md](README.md) - Getting started guide
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - Complete API reference
- [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) - Deployment guide
- [LIVE_SEARCH_GUIDE.md](LIVE_SEARCH_GUIDE.md) - Frontend guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design details
