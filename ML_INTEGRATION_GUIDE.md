"""
Django ML Model Integration Guide

This document explains how to integrate the ML model views into your Django project.
"""

# ==============================================================================
# STEP 1: Add to doctors/urls.py
# ==============================================================================

"""
File: doctors/urls.py

Add these imports and URL patterns:
"""

from django.urls import path
from . import ml_views

app_name = 'doctors'

urlpatterns = [
    # Existing URLs...
    
    # ML Model Prediction URLs
    path('predict/', ml_views.doctor_rating_predictor, name='predictor'),
    path('api/predict/', ml_views.api_predict_rating, name='api_predict'),
    path('api/health/', ml_views.model_health_check, name='health_check'),
]


# ==============================================================================
# STEP 2: Update doctor_search/settings.py
# ==============================================================================

"""
File: doctor_search/settings.py

Add ML configuration and logging:
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ML Models Configuration
ML_MODELS_DIR = os.path.join(BASE_DIR, 'models')
ML_LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Ensure directories exist
os.makedirs(ML_MODELS_DIR, exist_ok=True)
os.makedirs(ML_LOGS_DIR, exist_ok=True)

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name} {funcName} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(ML_LOGS_DIR, 'django.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'ml_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(ML_LOGS_DIR, 'ml_predictions.log'),
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'doctors': {
            'handlers': ['console', 'ml_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# ==============================================================================
# STEP 3: Update doctor_search/urls.py (if needed)
# ==============================================================================

"""
File: doctor_search/urls.py

Include the doctors URLs:
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('doctors.urls')),  # This includes doctors/urls.py
]


# ==============================================================================
# USAGE EXAMPLES
# ==============================================================================

# ============
# WEB FORM
# ============
"""
Access the web form at:
    http://localhost:8000/predict/

1. Select specialization from dropdown
2. Enter years of experience
3. Click "Predict Rating"
4. View the prediction result
"""


# ============
# API ENDPOINT
# ============
"""
Make a POST request to:
    http://localhost:8000/api/predict/

Example using curl:
    curl -X POST http://localhost:8000/api/predict/ \
      -H "Content-Type: application/json" \
      -d '{
        "specialization": "Cardiology",
        "experience_years": 10
      }'

Example using Python requests:
    import requests
    
    response = requests.post(
        'http://localhost:8000/api/predict/',
        json={
            'specialization': 'Cardiology',
            'experience_years': 10
        }
    )
    
    result = response.json()
    print(f"Predicted rating: {result['prediction']}")

Response (success):
    {
        "success": true,
        "prediction": 4.25,
        "specialization": "Cardiology",
        "experience_years": 10
    }

Response (error):
    {
        "success": false,
        "error": "Specialization 'Invalid' not recognized"
    }
"""


# ============
# HEALTH CHECK
# ============
"""
Check if model is loaded:
    http://localhost:8000/api/health/

Response:
    {
        "model_available": true,
        "encoder_available": true,
        "ready": true,
        "message": ""
    }
"""


# ==============================================================================
# INTEGRATION WITH EXISTING VIEWS
# ==============================================================================

"""
Example: Use prediction in doctor detail view
File: doctors/views.py
"""

from django.shortcuts import render, get_object_or_404
from .models import Doctor
from .ml_views import predict_doctor_rating

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # Get ML prediction
    prediction = predict_doctor_rating(
        specialization=doctor.specialization,
        experience_years=doctor.experience_years
    )
    
    context = {
        'doctor': doctor,
        'prediction': prediction
    }
    
    return render(request, 'doctors/detail.html', context)


# ==============================================================================
# INTEGRATION WITH API (Django REST Framework)
# ==============================================================================

"""
Example: Create API view using DRF
File: doctors/api_views.py
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .ml_views import predict_doctor_rating

@api_view(['POST'])
def doctor_prediction_api(request):
    specialization = request.data.get('specialization')
    experience_years = request.data.get('experience_years')
    
    if not specialization or experience_years is None:
        return Response(
            {'error': 'Missing specialization or experience_years'},
            status=400
        )
    
    result = predict_doctor_rating(specialization, experience_years)
    
    if result['success']:
        return Response(result, status=200)
    else:
        return Response(result, status=400)


# ==============================================================================
# TESTING
# ==============================================================================

"""
Create test file: doctors/test_ml_views.py
"""

from django.test import TestCase
from django.test.client import Client
from .ml_views import predict_doctor_rating
import json

class MLViewsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_prediction_form_get(self):
        """Test prediction form page loads"""
        response = self.client.get('/predict/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctors/predictor.html')
    
    def test_prediction_form_post(self):
        """Test prediction form submission"""
        response = self.client.post('/predict/', {
            'specialization': 'Cardiology',
            'experience_years': 10
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', response.context)
    
    def test_api_predict(self):
        """Test API prediction endpoint"""
        data = {
            'specialization': 'Cardiology',
            'experience_years': 10
        }
        response = self.client.post(
            '/api/predict/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['success'])
        self.assertIn('prediction', result)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn('ready', result)

# Run tests:
#   python manage.py test doctors.test_ml_views


# ==============================================================================
# PRODUCTION CONSIDERATIONS
# ==============================================================================

"""
1. Model Caching:
   - ModelLoader uses class variables to cache model and encoder
   - Models are loaded once and reused for all predictions
   - Reduces I/O overhead significantly

2. Error Handling:
   - FileNotFoundError if model files missing
   - ValueError if specialization not recognized
   - All errors logged to ML_LOGS_DIR

3. Performance:
   - First prediction loads model (~100ms)
   - Subsequent predictions very fast (~10ms)
   - Add Redis caching for prediction results if needed

4. Security:
   - Input validation on specialization
   - Experience years bounded (0-100)
   - CSRF protection on form submissions
   - Rate limiting recommended for API endpoints

5. Monitoring:
   - All predictions logged with inputs and outputs
   - Health check endpoint for monitoring
   - Log files auto-rotate at 10MB

6. Scaling:
   - Consider async tasks for batch predictions
   - Cache model in memory for high-traffic scenarios
   - Add monitoring/alerting for model accuracy
"""


# ==============================================================================
# TROUBLESHOOTING
# ==============================================================================

"""
1. "Model file not found" error:
   - Ensure model.pkl and encoder.pkl exist in models/ folder
   - Run train_model.py to generate them
   - Check file paths in settings.py

2. "Specialization not recognized" error:
   - Check specialization spelling exactly
   - Ensure it matches training data
   - See PredictionForm.SPECIALIZATION_CHOICES for valid options

3. Prediction not working:
   - Check logs in logs/ml_predictions.log
   - Run health check: curl http://localhost:8000/api/health/
   - Verify Django server is running

4. Slow predictions:
   - First prediction is slower (model loading)
   - Check server logs for performance issues
   - Consider model optimization if consistently slow

5. CSRF token error:
   - Ensure {% csrf_token %} in form template
   - Check CSRF middleware is enabled
   - For API calls, use X-CSRFToken header
"""


# ==============================================================================
# NEXT STEPS
# ==============================================================================

"""
1. Copy ml_views.py to doctors/ folder
2. Copy ml_urls.py content to doctors/urls.py
3. Copy predictor.html to doctors/templates/doctors/
4. Update settings.py with ML configuration
5. Ensure model.pkl and encoder.pkl exist
6. Run migrations: python manage.py migrate
7. Test: python manage.py runserver
8. Access: http://localhost:8000/predict/
"""
