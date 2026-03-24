"""
ML Model Usage Examples

This file demonstrates various ways to use the ML model prediction views
in your Django project.
"""

# ==============================================================================
# EXAMPLE 1: Direct Function Usage
# ==============================================================================

"""
Use the predict_doctor_rating function directly in your code
"""

from doctors.ml_views import predict_doctor_rating

# Make a prediction
result = predict_doctor_rating(
    specialization='Cardiology',
    experience_years=10
)

if result['success']:
    rating = result['prediction']
    print(f"Predicted rating: {rating} stars")
    # Output: Predicted rating: 4.25 stars
else:
    print(f"Error: {result['error']}")


# ==============================================================================
# EXAMPLE 2: In Django Shell
# ==============================================================================

"""
python manage.py shell

>>> from doctors.ml_views import predict_doctor_rating
>>> 
>>> # Make prediction
>>> result = predict_doctor_rating('Neurology', 8)
>>> print(result)
{
    'success': True,
    'prediction': 3.95,
    'specialization': 'Neurology',
    'experience_years': 8
}
>>> 
>>> # Use in a loop
>>> specialties = ['Cardiology', 'Dermatology', 'Surgery']
>>> for specialty in specialties:
...     result = predict_doctor_rating(specialty, 10)
...     print(f"{specialty}: {result['prediction']}⭐")
Cardiology: 4.25⭐
Dermatology: 3.85⭐
Surgery: 4.15⭐
"""


# ==============================================================================
# EXAMPLE 3: In Django Views
# ==============================================================================

"""
File: doctors/views.py
Use predictions in existing doctor views
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Doctor
from .ml_views import predict_doctor_rating

# Function-based view
def doctor_detail(request, doctor_id):
    """Display doctor details with predicted rating"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    # Get ML prediction
    prediction_result = predict_doctor_rating(
        specialization=doctor.specialization,
        experience_years=doctor.experience_years
    )
    
    context = {
        'doctor': doctor,
        'predicted_rating': prediction_result.get('prediction') if prediction_result['success'] else None,
        'is_prediction': True,
    }
    
    return render(request, 'doctors/detail.html', context)


# Class-based view
class DoctorDetailView(DetailView):
    """Alternative class-based view with prediction"""
    model = Doctor
    template_name = 'doctors/detail.html'
    context_object_name = 'doctor'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.get_object()
        
        # Add prediction to context
        prediction_result = predict_doctor_rating(
            specialization=doctor.specialization,
            experience_years=doctor.experience_years
        )
        
        context['predicted_rating'] = (
            prediction_result.get('prediction')
            if prediction_result['success']
            else None
        )
        context['is_prediction'] = True
        
        return context


# ==============================================================================
# EXAMPLE 4: In Django REST Framework API
# ==============================================================================

"""
File: doctors/api_views.py
Integrate with existing DRF endpoints
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import DoctorSerializer
from .ml_views import predict_doctor_rating

@api_view(['GET'])
def doctor_with_prediction(request, doctor_id):
    """API endpoint: Get doctor with ML prediction"""
    from .models import Doctor
    
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response(
            {'error': 'Doctor not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Serialize doctor
    serializer = DoctorSerializer(doctor)
    data = serializer.data
    
    # Add ML prediction
    prediction = predict_doctor_rating(
        specialization=doctor.specialization,
        experience_years=doctor.experience_years
    )
    
    if prediction['success']:
        data['ml_predicted_rating'] = prediction['prediction']
        data['ml_prediction_available'] = True
    else:
        data['ml_prediction_available'] = False
        data['ml_error'] = prediction['error']
    
    return Response(data, status=status.HTTP_200_OK)


# ==============================================================================
# EXAMPLE 5: Batch Predictions
# ==============================================================================

"""
File: doctors/management/commands/batch_predict.py
Create a management command for batch predictions
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from doctors.models import Doctor
from doctors.ml_views import predict_doctor_rating
import csv

class Command(BaseCommand):
    help = 'Run batch predictions for all doctors'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='predictions.csv',
            help='Output CSV file'
        )
    
    def handle(self, *args, **options):
        doctors = Doctor.objects.all()
        output_file = options['output']
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Doctor ID',
                'Name',
                'Specialization',
                'Experience',
                'Actual Rating',
                'ML Predicted Rating',
                'Difference'
            ])
            
            for doctor in doctors:
                prediction = predict_doctor_rating(
                    specialization=doctor.specialization,
                    experience_years=doctor.experience_years
                )
                
                if prediction['success']:
                    diff = abs(
                        doctor.average_rating - prediction['prediction']
                    )
                    writer.writerow([
                        doctor.id,
                        doctor.name,
                        doctor.specialization,
                        doctor.experience_years,
                        doctor.average_rating,
                        prediction['prediction'],
                        diff
                    ])
                    self.stdout.write(
                        f"✓ {doctor.name}: {prediction['prediction']:.2f}⭐"
                    )
                else:
                    self.stdout.write(
                        f"✗ {doctor.name}: {prediction['error']}"
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f"\nPredictions saved to {output_file}")
        )

# Run with: python manage.py batch_predict --output=predictions.csv


# ==============================================================================
# EXAMPLE 6: Debugging/Development Usage
# ==============================================================================

"""
Test predictions interactively
"""

from doctors.ml_views import ModelLoader, predict_doctor_rating
import json

# Check if models are loaded
try:
    model = ModelLoader.get_model()
    encoder = ModelLoader.get_encoder()
    print("✓ Models loaded successfully")
except Exception as e:
    print(f"✗ Error loading models: {e}")

# Test all specializations
specializations = [
    'Cardiology',
    'Dermatology',
    'Neurology',
    'Orthopedics',
    'Pediatrics',
    'Surgery',
    'General Medicine',
    'Psychiatry'
]

print("\nTesting predictions for all specializations (10 years experience):")
print("-" * 60)

for specialty in specializations:
    result = predict_doctor_rating(specialty, 10)
    if result['success']:
        print(f"{specialty:20} → {result['prediction']:.2f}⭐")
    else:
        print(f"{specialty:20} → ERROR: {result['error']}")

# Test experience levels for one specialty
print("\n\nTesting different experience levels (Cardiology):")
print("-" * 60)

experience_levels = [1, 5, 10, 15, 20]
for years in experience_levels:
    result = predict_doctor_rating('Cardiology', years)
    if result['success']:
        print(f"{years:2} years experience → {result['prediction']:.2f}⭐")
    else:
        print(f"{years:2} years experience → ERROR")


# ==============================================================================
# EXAMPLE 7: Async/Celery Integration (Optional)
# ==============================================================================

"""
File: doctors/tasks.py
Create async tasks for predictions
"""

from celery import shared_task
from .ml_views import predict_doctor_rating
from .models import Doctor
import logging

logger = logging.getLogger(__name__)

@shared_task
def predict_and_store_rating(doctor_id):
    """Async task to predict rating and store"""
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        
        prediction = predict_doctor_rating(
            specialization=doctor.specialization,
            experience_years=doctor.experience_years
        )
        
        if prediction['success']:
            # Store prediction (add field to Doctor model first)
            # doctor.ml_predicted_rating = prediction['prediction']
            # doctor.save()
            logger.info(f"Prediction for doctor {doctor_id}: {prediction['prediction']}")
        else:
            logger.error(f"Prediction failed for doctor {doctor_id}")
    
    except Doctor.DoesNotExist:
        logger.error(f"Doctor {doctor_id} not found")

@shared_task
def batch_predict_all_doctors():
    """Async task to predict ratings for all doctors"""
    doctors = Doctor.objects.all()
    for doctor in doctors:
        predict_and_store_rating.delay(doctor.id)
    
    return f"Batch prediction started for {doctors.count()} doctors"

# Usage:
# predict_and_store_rating.delay(doctor_id)
# batch_predict_all_doctors.delay()


# ==============================================================================
# EXAMPLE 8: API Client Usage (External)
# ==============================================================================

"""
Python client for API consumption
"""

import requests
import json

class DoctorPredictorClient:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
    
    def predict(self, specialization, experience_years):
        """Make prediction via API"""
        url = f"{self.base_url}/api/predict/"
        
        payload = {
            'specialization': specialization,
            'experience_years': experience_years
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def health_check(self):
        """Check if service is ready"""
        url = f"{self.base_url}/api/health/"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {
                'ready': False,
                'message': str(e)
            }

# Usage:
if __name__ == '__main__':
    client = DoctorPredictorClient()
    
    # Check service health
    health = client.health_check()
    print(f"Service ready: {health.get('ready', False)}")
    
    # Make prediction
    result = client.predict('Cardiology', 10)
    if result['success']:
        print(f"Predicted rating: {result['prediction']}⭐")
    else:
        print(f"Error: {result['error']}")


# ==============================================================================
# EXAMPLE 9: JavaScript/Frontend Usage
# ==============================================================================

"""
HTML/JavaScript to call prediction API
"""

# HTML snippet:
"""
<script>
async function predictRating() {
    const specialty = document.getElementById('specialty').value;
    const experience = document.getElementById('experience').value;
    
    try {
        const response = await fetch('/api/predict/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                specialization: specialty,
                experience_years: parseInt(experience)
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('result').innerHTML = 
                `Rating: ${data.prediction}⭐`;
        } else {
            document.getElementById('result').innerHTML = 
                `Error: ${data.error}`;
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie.length > 0) {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
</script>
"""


# ==============================================================================
# EXAMPLE 10: Testing
# ==============================================================================

"""
File: doctors/test_predictions.py
Comprehensive test examples
"""

from django.test import TestCase, Client
from .models import Doctor
from .ml_views import predict_doctor_rating
import json

class PredictionTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.doctor = Doctor.objects.create(
            name='Dr. Test',
            specialization='Cardiology',
            experience_years=10,
            location='Test City',
            contact='123-456-7890',
            email='test@example.com'
        )
    
    def test_direct_prediction(self):
        """Test direct function prediction"""
        result = predict_doctor_rating('Cardiology', 10)
        self.assertTrue(result['success'])
        self.assertIn('prediction', result)
        self.assertGreaterEqual(result['prediction'], 1)
        self.assertLessEqual(result['prediction'], 5)
    
    def test_invalid_specialization(self):
        """Test with invalid specialization"""
        result = predict_doctor_rating('InvalidSpecialty', 10)
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_web_form(self):
        """Test web form prediction"""
        response = self.client.post('/predict/', {
            'specialization': 'Cardiology',
            'experience_years': 10
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', response.context)
        self.assertTrue(response.context['result']['success'])
    
    def test_api_prediction(self):
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

# Run: python manage.py test doctors.test_predictions
