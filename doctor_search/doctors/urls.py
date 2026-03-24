from django.urls import path
from . import views
# from .ml_views import doctor_rating_predictor, api_predict_rating

urlpatterns = [
    # ==================== AUTHENTICATION ====================
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # ==================== USER PROFILE & DASHBOARD ====================
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('my-appointments/', views.my_appointments_view, name='my_appointments'),
    path('my-reviews/', views.my_reviews_view, name='my_reviews'),
    
    # ==================== REVIEWS ====================
    path('review/<int:doctor_id>/', views.write_review_view, name='write_review'),
    
    # ==================== SEARCH & APPOINTMENTS ====================
    path('', views.search_doctors, name='search'),
    path('home/', views.search_doctors, name='home'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment_for_doctor'),
    path('confirmation/<int:appointment_id>/', views.appointment_confirmation, name='appointment_confirmation'),
    
    # ==================== ML PREDICTION ====================
    # Uncomment if ml_views.py exists
    # path('predict/', doctor_rating_predictor, name='predict'),
    # path('api/predict/', api_predict_rating, name='api_predict'),
]