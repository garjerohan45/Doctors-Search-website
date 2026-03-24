# Doctor Search System - Troubleshooting & FAQ

> Comprehensive troubleshooting guide and frequently asked questions for the Doctor Search System.

---

## ❓ FAQs

### General Questions

#### Q: What Python version do I need?
**A:** Python 3.8 or higher. The project uses Django 6.0.3 which supports Python 3.10+. You can check your version with:
```bash
python --version
```

#### Q: Can I use this with a different database?
**A:** Yes. By default it uses SQLite (good for development). For production, configure PostgreSQL:
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'doctor_search',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Then install: `pip install psycopg2-binary`

#### Q: How do I add more doctors?
**A:** Use one of these methods:

**Method 1: Django Shell**
```bash
python manage.py shell
```
```python
from doctors.models import Doctor
Doctor.objects.create(
    name="Dr. Sarah Connor",
    specialization="Neurology",
    location="Los Angeles",
    experience=8,
    contact="555-5678",
    email="sarah@example.com",
    bio="Expert in neurology",
    qualification="MD, Neurology",
    clinic_name="Connor Medical"
)
```

**Method 2: Django Admin**
1. Go to http://localhost:8000/admin/
2. Log in with superuser
3. Click "Doctors" → "Add Doctor"
4. Fill in form and save

**Method 3: Bulk Upload (via fixture)**
Create `doctors/fixtures/doctors.json`:
```json
[
  {
    "model": "doctors.doctor",
    "pk": 1,
    "fields": {
      "name": "Dr. John Smith",
      "specialization": "Cardiology",
      "location": "New York",
      "experience": 10,
      "contact": "555-1234",
      "email": "john@example.com",
      "bio": "Expert cardiologist",
      "qualification": "MD, Cardiology",
      "clinic_name": "Heart Care Clinic"
    }
  }
]
```
Then load: `python manage.py loaddata doctors`

---

## 🐛 Troubleshooting Issues

### Setup & Installation Issues

#### ❌ "ModuleNotFoundError: No module named 'django'"
**Cause:** Django not installed in your environment

**Solutions:**
```bash
# Make sure virtual environment is activated
# Windows
myvenv\Scripts\activate
# Mac/Linux
source myvenv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Verify installation
python -m django --version
```

#### ❌ "No such table: doctors_doctor"
**Cause:** Database migrations not run

**Solution:**
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Verify
python manage.py showmigrations
```

#### ❌ "sqlite3.DatabaseError: database disk image is malformed"
**Cause:** Corrupted database file

**Solution:**
```bash
# Delete corrupted database (WARNING: loses all data)
del db.sqlite3

# Recreate database
python manage.py migrate

# Recreate superuser
python manage.py createsuperuser
```

#### ❌ "Address already in use" on port 8000
**Cause:** Another process using port 8000

**Solutions:**
```bash
# Windows - find and kill process
netstat -ano | findstr :8000
taskkill /PID {pid} /F

# Mac/Linux - find and kill process
lsof -i :8000
kill -9 {pid}

# OR use different port
python manage.py runserver 8001
```

---

### Authentication & API Issues

#### ❌ "Authentication credentials were not provided"
**Cause:** API request missing token for protected endpoint

**Solution:**
1. Register at `/api/register/`
2. Get token from `/api/auth-token/`
3. Include in request headers:
```bash
Authorization: Token YOUR_TOKEN_HERE
```

Example with curl:
```bash
curl http://localhost:8000/api/appointments/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

#### ❌ "User with this username already exists"
**Cause:** Username taken during registration

**Solution:**
- Use a different username
- Or reset database and run migrations again

#### ❌ "User has no profile"
**Cause:** UserProfile not auto-created

**Solution:**
- Check that `doctors/signals.py` is imported in `doctors/apps.py`
- Verify signal is defined correctly
- Create manually:
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
from doctors.models import UserProfile
user = User.objects.get(username='john_doe')
UserProfile.objects.create(user=user)
```

#### ❌ "Token 'xxx' is invalid or expired"
**Cause:** Token not recognized or invalid

**Solution:**
1. Verify token was generated correctly
2. Get new token from `/api/auth-token/`
3. Check token in database:
```bash
python manage.py shell
```
```python
from rest_framework.authtoken.models import Token
Token.objects.all()  # List all tokens
Token.objects.filter(key='xxx')  # Find specific token
```

---

### Data & Model Issues

#### ❌ "Appointment.date: Ensure this value is greater than or equal to the current date"
**Cause:** Trying to book appointment in the past

**Solution:**
- Always book appointments for future dates
- Check current date: `from datetime import date; print(date.today())`

#### ❌ "The fields doctor, user of Review must make a unique set"
**Cause:** User already reviewed this doctor

**Solution:**
- Each user can only leave one review per doctor
- Update existing review instead
- Or delete old review and create new one:
```bash
python manage.py shell
```
```python
from doctors.models import Review
# Delete existing review
Review.objects.filter(doctor_id=1, user_id=1).delete()
# Create new one
Review.objects.create(doctor_id=1, user_id=1, rating=5, ...)
```

#### ❌ "Doctor average_rating is incorrect"
**Cause:** Rating not updated after review creation/deletion

**Solution:**
- Check that `update_doctor_rating()` signal is working
- Manual recalculation:
```bash
python manage.py shell
```
```python
from django.db.models import Avg, Count
from doctors.models import Doctor, Review

doctor = Doctor.objects.get(id=1)
ratings = Review.objects.filter(doctor=doctor)
doctor.average_rating = ratings.aggregate(Avg('rating'))['rating__avg'] or 0
doctor.total_reviews = ratings.count()
doctor.save()
```

---

### Frontend & Live Search Issues

#### ❌ Live search not working / no results appearing
**Cause:** JavaScript not running or API not accessible

**Solutions:**
1. Check browser console (F12 → Console tab) for errors
2. Verify API is running: `python manage.py runserver`
3. Check file exists: `doctors/static/js/live_search.js`
4. Verify script included in template:
   ```html
   <script src="{% static 'js/live_search.js' %}"></script>
   ```
5. Check API response manually:
   ```bash
   curl "http://localhost:8000/api/doctors/search/?name=john"
   ```

#### ❌ "Failed to fetch" error in live search
**Cause:** CORS issue or API endpoint not accessible

**Solutions:**
1. Check if API is running
2. Check URL is correct
3. Add error logging to live_search.js:
   ```javascript
   fetch(url)
     .catch(error => console.error('Fetch error:', error));
   ```

#### ❌ Loading spinner stays visible forever
**Cause:** API not responding or JavaScript error

**Solutions:**
1. Check browser console (F12)
2. Check Django server logs
3. Add timeout to fetch:
   ```javascript
   const controller = new AbortController();
   const timeout = setTimeout(() => controller.abort(), 5000);
   fetch(url, { signal: controller.signal })
     .finally(() => clearTimeout(timeout));
   ```

---

### Performance Issues

#### ❌ API endpoints responding slowly (>1 second)
**Cause:** Too many database queries

**Solutions:**
1. Check with Django Debug Toolbar:
   ```bash
   pip install django-debug-toolbar
   ```
   - Add to `INSTALLED_APPS` and `MIDDLEWARE`
   - View `localhost:8000/__debug__/` when DEBUG=True

2. Optimize queries using select_related/prefetch_related:
   ```python
   # Bad
   appointments = Appointment.objects.all()
   
   # Good
   appointments = Appointment.objects.select_related('doctor', 'patient')
   ```

#### ❌ High database file size (db.sqlite3 > 100MB)
**Cause:** Old data accumulation

**Solutions:**
1. Clean up old data:
   ```bash
   python manage.py shell
   ```
   ```python
   from doctors.models import Appointment
   from datetime import datetime, timedelta
   
   # Delete appointments older than 1 month
   old_date = datetime.now() - timedelta(days=30)
   Appointment.objects.filter(date__lt=old_date).delete()
   ```

2. Optimize database:
   ```bash
   python manage.py dbshell
   VACUUM;
   ```

#### ❌ "Too many open files" error
**Cause:** File descriptor limit exceeded

**Solution (Linux/Mac):**
```bash
# Check current limit
ulimit -n

# Increase limit
ulimit -n 2048
```

---

### Deployment Issues

#### ❌ "disallowed host at ..."
**Cause:** Missing ALLOWED_HOSTS configuration

**Solution:**
```python
# settings.py
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', '127.0.0.1']
```

#### ❌ "DisallowedRedirect at /api/ 'http://example.com/api/' is not an allowed redirect target"
**Cause:** Redirect URL not in ALLOWED_HOSTS

**Solution:**
```python
# settings.py
ALLOWED_HOSTS = ['example.com', 'www.example.com']
```

#### ❌ Static files (CSS/JavaScript) not loading (404)
**Cause:** Static files not collected

**Solution:**
```bash
python manage.py collectstatic --noinput
```

Configuration:
```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

#### ❌ "connection refused" when connecting to PostgreSQL
**Cause:** Database server not running or wrong credentials

**Solution:**
1. Check PostgreSQL is running:
   ```bash
   # Windows
   pg_isready
   
   # Mac
   brew services list | grep postgres
   ```

2. Verify connection details in settings.py
3. Test connection:
   ```bash
   psql -U postgres -h localhost -d doctor_search
   ```

---

### Migration Issues

#### ❌ "The field 'doctors.Doctor.average_rating' does not have a default"
**Cause:** Adding non-nullable field to existing table

**Solution:**
1. Provide default value in migration
2. Or make field nullable: `null=True, blank=True`
3. In migration file:
   ```python
   migrations.AddField(
       model_name='doctor',
       name='average_rating',
       field=models.FloatField(default=0.0),
   ),
   ```

#### ❌ "Column 'xxx' does not exist"
**Cause:** Code references field that's not in database

**Solution:**
1. Make and apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Or rollback code to match database

#### ❌ "Cannot add a NOT NULL column without a default"
**Cause:** Migration trying to add required field

**Solution:**
In your migration, add default:
```python
migrations.AddField(
    model_name='model',
    name='field',
    field=models.CharField(max_length=100, default=''),
),
```

---

## 🔍 Debugging Techniques

### Enable SQL Logging
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Check Active Queries
```bash
python manage.py shell
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    from doctors.models import Doctor
    list(Doctor.objects.all())

print(f"Queries: {len(context)}")
for query in context:
    print(query['sql'])
```

### Test API Endpoints Locally
```bash
# Use Python requests library
pip install requests

python -c "
import requests
import json

# Get doctors
response = requests.get('http://localhost:8000/api/doctors/')
print(response.status_code)
print(json.dumps(response.json(), indent=2))
"
```

### Monitor Server in Real-Time
```bash
# Terminal 1: Watch for errors
tail -f /var/log/django.log

# Terminal 2: Monitor database
watch -n 1 'sqlite3 db.sqlite3 "SELECT COUNT(*) FROM doctors_doctor;"'

# Terminal 3: Run server
python manage.py runserver
```

---

## 📝 Common Code Fixes

### Fix: Import Error
```python
# ❌ Wrong
from models import Doctor

# ✅ Correct
from doctors.models import Doctor
```

### Fix: Query Filter
```python
# ❌ Wrong - uses = instead of __exact or ==
doctors = Doctor.objects.filter(name="John")  # Works but unclear

# ✅ Better - explicit
doctors = Doctor.objects.filter(name__exact="John")  # Exact match
doctors = Doctor.objects.filter(name__icontains="john")  # Case-insensitive partial
```

### Fix: Serializer Nesting
```python
# ❌ Wrong - nested serializer not instantiated
doctor_data = {
    'doctor': DoctorSerializer  # Wrong!
}

# ✅ Correct - nested serializer with many parameter
doctor_data = {
    'doctor': DoctorSerializer(instance, many=True)  # Correct
}
```

### Fix: Signal Not Firing
```python
# ❌ Wrong - signal not registered
# doctors/signals.py exists but not imported

# ✅ Correct - import in ready()
# doctors/apps.py
def ready(self):
    import doctors.signals
```

---

## 📊 Quick Health Check Script

Save as `health_check.py` in project root:

```python
#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctor_search.settings')
django.setup()

from django.db import connection
from doctors.models import Doctor, Appointment, Review, UserProfile
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

print("✅ Doctor Search System - Health Check")
print("=" * 50)

# Database connection
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    print("✅ Database: Connected")
except Exception as e:
    print(f"❌ Database: {e}")

# Models
print(f"✅ Doctors: {Doctor.objects.count()} in database")
print(f"✅ Users: {User.objects.count()} in database")
print(f"✅ Appointments: {Appointment.objects.count()} in database")
print(f"✅ Reviews: {Review.objects.count()} in database")
print(f"✅ Profiles: {UserProfile.objects.count()} in database")
print(f"✅ Tokens: {Token.objects.count()} in database")

# Sample data
top_doctors = Doctor.objects.order_by('-average_rating')[:3]
print("\n📊 Top Rated Doctors:")
for doc in top_doctors:
    print(f"   - {doc.name} ({doc.average_rating}⭐, {doc.total_reviews} reviews)")

print("\n=" * 50)
print("✅ System appears healthy!")
```

Run with: `python health_check.py`

---

## 📞 Getting Help

1. **Check logs**: `python manage.py check`
2. **Django documentation**: https://docs.djangoproject.com/
3. **Django REST Framework**: https://www.django-rest-framework.org/
4. **Stack Overflow**: Tag your question with [django]
5. **GitHub Issues**: Create issue with error trace

---

## Next Steps

- See [README.md](README.md) for setup instructions
- See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API reference
- See [PRODUCTION_GUIDE.md](PRODUCTION_GUIDE.md) for deployment
