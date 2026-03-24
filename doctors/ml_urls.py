"""
URL Configuration for ML Model Views

Add these URLs to your project's URL configuration.
"""

from django.urls import path
from . import ml_views

app_name = 'ml_predictor'

urlpatterns = [
    # Web interface for predictions
    path(
        'predict/',
        ml_views.doctor_rating_predictor,
        name='predictor'
    ),
    
    # Alternative: Class-based view
    # path(
    #     'predict/',
    #     ml_views.DoctorRatingPredictorView.as_view(),
    #     name='predictor'
    # ),
    
    # API endpoint for programmatic access
    path(
        'api/predict/',
        ml_views.api_predict_rating,
        name='api_predict'
    ),
    
    # Health check endpoint
    path(
        'api/health/',
        ml_views.model_health_check,
        name='health_check'
    ),
]

# Instructions:
# 1. In doctors/urls.py, add:
#    from . import ml_views
#    urlpatterns += [
#        path('ml/', include('doctors.urls')),  # Or add above patterns directly
#    ]
#
# 2. In doctor_search/urls.py, add:
#    from django.urls import path, include
#    urlpatterns = [
#        path('api/', include('doctors.urls')),
#    ]
#
# 3. Then access at:
#    - Web form: http://localhost:8000/api/predict/
#    - API: POST to http://localhost:8000/api/api/predict/
#    - Health: http://localhost:8000/api/api/health/
