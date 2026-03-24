from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .api_views import (
    DoctorViewSet, AppointmentViewSet, ReviewViewSet,
    UserProfileViewSet, register_user
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'profile', UserProfileViewSet, basename='profile')

# URL patterns for the API
urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user, name='register'),
    path('auth-token/', obtain_auth_token, name='auth-token'),
    path('auth/', include('rest_framework.urls')),
]
