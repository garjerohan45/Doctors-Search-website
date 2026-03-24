"""
Django Views for ML Model Integration

This module contains views that load and use the trained ML model
to make predictions about doctor ratings.
"""

import os
import pickle
import logging
from pathlib import Path

from django import forms
from django.shortcuts import render
from django.views import View
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)


class PredictionForm(forms.Form):
    """Form for collecting prediction input from users."""
    
    SPECIALIZATION_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Dermatology', 'Dermatology'),
        ('Neurology', 'Neurology'),
        ('Orthopedics', 'Orthopedics'),
        ('Pediatrics', 'Pediatrics'),
        ('Surgery', 'Surgery'),
        ('General Medicine', 'General Medicine'),
        ('Psychiatry', 'Psychiatry'),
    ]
    
    specialization = forms.ChoiceField(
        choices=SPECIALIZATION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select specialization'
        }),
        label='Doctor Specialization'
    )
    
    experience_years = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter years of experience',
            'type': 'number'
        }),
        label='Years of Experience'
    )


class ModelLoader:
    """Utility class to load and cache ML model and encoder."""
    
    _model = None
    _encoder = None
    
    @classmethod
    def get_model(cls):
        """Load and cache the trained model."""
        if cls._model is None:
            model_path = os.path.join(settings.BASE_DIR, 'models', 'model.pkl')
            
            if not os.path.exists(model_path):
                logger.error(f"Model file not found at {model_path}")
                raise FileNotFoundError(f"Model not found: {model_path}")
            
            try:
                with open(model_path, 'rb') as f:
                    cls._model = pickle.load(f)
                logger.info(f"Model loaded successfully from {model_path}")
            except Exception as e:
                logger.error(f"Error loading model: {str(e)}")
                raise
        
        return cls._model
    
    @classmethod
    def get_encoder(cls):
        """Load and cache the LabelEncoder."""
        if cls._encoder is None:
            encoder_path = os.path.join(settings.BASE_DIR, 'models', 'encoder.pkl')
            
            if not os.path.exists(encoder_path):
                logger.error(f"Encoder file not found at {encoder_path}")
                raise FileNotFoundError(f"Encoder not found: {encoder_path}")
            
            try:
                with open(encoder_path, 'rb') as f:
                    cls._encoder = pickle.load(f)
                logger.info(f"Encoder loaded successfully from {encoder_path}")
            except Exception as e:
                logger.error(f"Error loading encoder: {str(e)}")
                raise
        
        return cls._encoder


def predict_doctor_rating(specialization, experience_years):
    """
    Predict doctor rating based on specialization and experience.
    
    Args:
        specialization (str): Doctor's specialization
        experience_years (int): Years of experience
        
    Returns:
        dict: Contains 'success' (bool), 'prediction' (float), and optional 'error' (str)
    """
    try:
        # Load model and encoder
        model = ModelLoader.get_model()
        encoder = ModelLoader.get_encoder()
        
        # Encode specialization
        try:
            specialty_encoded = encoder.transform([specialization])[0]
        except ValueError as e:
            logger.warning(f"Specialization '{specialization}' not recognized: {e}")
            return {
                'success': False,
                'error': f"Specialization '{specialization}' not recognized"
            }
        
        # Prepare input features
        features = [[specialty_encoded, experience_years]]
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        # Ensure prediction is within valid range (1-5 for ratings)
        prediction = max(1.0, min(5.0, prediction))
        
        logger.info(
            f"Prediction made: specialty={specialization}, "
            f"experience={experience_years}, prediction={prediction:.2f}"
        )
        
        return {
            'success': True,
            'prediction': round(prediction, 2),
            'specialization': specialization,
            'experience_years': experience_years
        }
    
    except FileNotFoundError as e:
        logger.error(f"Model file error: {e}")
        return {
            'success': False,
            'error': 'Prediction model not available. Please ensure model files exist.'
        }
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return {
            'success': False,
            'error': f'An error occurred during prediction: {str(e)}'
        }


@require_http_methods(["GET", "POST"])
def doctor_rating_predictor(request):
    """
    View to display prediction form and handle predictions.
    
    GET: Display the prediction form
    POST: Process the form and return prediction
    """
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        
        if form.is_valid():
            # Extract cleaned data
            specialization = form.cleaned_data['specialization']
            experience_years = form.cleaned_data['experience_years']
            
            # Get prediction
            result = predict_doctor_rating(specialization, experience_years)
            
            # Prepare context with result
            context = {
                'form': form,
                'result': result,
                'has_result': True
            }
            
            # If AJAX request, return JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(result)
            
            # Otherwise, render template with result
            return render(request, 'doctors/predictor.html', context)
        
        else:
            context = {
                'form': form,
                'has_result': False,
                'errors': form.errors
            }
            return render(request, 'doctors/predictor.html', context)
    
    else:
        # GET request - display empty form
        form = PredictionForm()
        context = {
            'form': form,
            'has_result': False
        }
        return render(request, 'doctors/predictor.html', context)


class DoctorRatingPredictorView(View):
    """Class-based view for doctor rating prediction (alternative approach)."""
    
    template_name = 'doctors/predictor.html'
    form_class = PredictionForm
    
    def get(self, request):
        """Display the prediction form."""
        form = self.form_class()
        context = {
            'form': form,
            'has_result': False
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        """Process prediction request."""
        form = self.form_class(request.POST)
        
        if form.is_valid():
            specialization = form.cleaned_data['specialization']
            experience_years = form.cleaned_data['experience_years']
            
            # Get prediction
            result = predict_doctor_rating(specialization, experience_years)
            
            context = {
                'form': form,
                'result': result,
                'has_result': True
            }
            
            # Handle AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(result)
            
            return render(request, self.template_name, context)
        
        context = {
            'form': form,
            'has_result': False,
            'errors': form.errors
        }
        return render(request, self.template_name, context)


@require_http_methods(["POST"])
def api_predict_rating(request):
    """
    API endpoint for programmatic access to predictions.
    
    Expects JSON POST data:
    {
        "specialization": "Cardiology",
        "experience_years": 10
    }
    
    Returns JSON:
    {
        "success": true,
        "prediction": 4.25,
        "specialization": "Cardiology",
        "experience_years": 10
    }
    """
    import json
    
    try:
        # Parse JSON request
        data = json.loads(request.body)
        
        specialization = data.get('specialization')
        experience_years = data.get('experience_years')
        
        # Validate input
        if not specialization or experience_years is None:
            return JsonResponse({
                'success': False,
                'error': 'Missing required fields: specialization, experience_years'
            }, status=400)
        
        # Validate experience_years is integer
        try:
            experience_years = int(experience_years)
        except (TypeError, ValueError):
            return JsonResponse({
                'success': False,
                'error': 'experience_years must be an integer'
            }, status=400)
        
        # Get prediction
        result = predict_doctor_rating(specialization, experience_years)
        
        status_code = 200 if result['success'] else 400
        return JsonResponse(result, status=status_code)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON in request body'
        }, status=400)
    
    except Exception as e:
        logger.error(f"API prediction error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def model_health_check(request):
    """
    Health check endpoint to verify model files exist and are loadable.
    
    Returns JSON status of model availability.
    """
    status = {
        'model_available': False,
        'encoder_available': False,
        'message': ''
    }
    
    try:
        model = ModelLoader.get_model()
        status['model_available'] = True
        logger.info("Model health check: OK")
    except FileNotFoundError:
        status['message'] = 'Model file not found'
    except Exception as e:
        status['message'] = f'Error loading model: {str(e)}'
    
    try:
        encoder = ModelLoader.get_encoder()
        status['encoder_available'] = True
    except FileNotFoundError:
        status['message'] = 'Encoder file not found'
    except Exception as e:
        status['message'] = f'Error loading encoder: {str(e)}'
    
    status['ready'] = status['model_available'] and status['encoder_available']
    return JsonResponse(status)
