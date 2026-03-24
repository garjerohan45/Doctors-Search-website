from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from .models import Doctor, Appointment, UserProfile, Review
from .forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserProfileForm,
    AppointmentForm,
    ReviewForm
)


# ==================== AUTHENTICATION VIEWS ====================

@require_http_methods(["GET", "POST"])
@csrf_protect
def register_view(request):
    """
    User registration view.
    Handles GET (display form) and POST (process registration).
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(
                    request,
                    f'✅ Registration successful! Welcome {user.username}. Please login to continue.'
                )
                return redirect('login')
            except Exception as e:
                messages.error(request, f'❌ Error: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'page_title': 'Register',
    }
    return render(request, 'doctors/register.html', context)


@require_http_methods(["GET", "POST"])
@csrf_protect
def login_view(request):
    """
    User login view.
    Handles GET (display form) and POST (process login).
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = None
            
            # Try to authenticate with username or email
            if User.objects.filter(username=username).exists():
                user = authenticate(request, username=username, password=password)
            elif User.objects.filter(email=username).exists():
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'✅ Welcome {user.first_name or user.username}!')
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, '❌ Invalid username/email or password.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = UserLoginForm()
    
    context = {
        'form': form,
        'page_title': 'Login',
    }
    return render(request, 'doctors/login.html', context)


@login_required(login_url='login')
def logout_view(request):
    """
    User logout view.
    Logs out the current user and redirects to home.
    """
    logout(request)
    messages.success(request, '✅ Logged out successfully.')
    return redirect('home')


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def profile_view(request):
    """
    User profile view.
    Displays user information and allows editing profile.
    """
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, '✅ Profile updated successfully!')
                return redirect('profile')
            except Exception as e:
                messages.error(request, f'❌ Error: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    
    context = {
        'form': form,
        'profile': profile,
        'page_title': f'{request.user.first_name or request.user.username}\'s Profile',
    }
    return render(request, 'doctors/profile.html', context)


@login_required(login_url='login')
def dashboard_view(request):
    """
    User dashboard showing appointments and reviews.
    """
    user_appointments = Appointment.objects.filter(patient=request.user).select_related('doctor')
    user_reviews = Review.objects.filter(user=request.user).select_related('doctor')
    profile = get_object_or_404(UserProfile, user=request.user)
    
    total_appointments = user_appointments.count()
    completed_appointments = user_appointments.filter(status='completed').count()
    pending_appointments = user_appointments.filter(status='pending').count()
    total_reviews = user_reviews.count()
    
    recent_appointments = user_appointments[:5]
    recent_reviews = user_reviews[:5]
    
    context = {
        'profile': profile,
        'total_appointments': total_appointments,
        'completed_appointments': completed_appointments,
        'pending_appointments': pending_appointments,
        'total_reviews': total_reviews,
        'recent_appointments': recent_appointments,
        'recent_reviews': recent_reviews,
        'page_title': 'My Dashboard',
    }
    return render(request, 'doctors/dashboard.html', context)


@login_required(login_url='login')
def my_appointments_view(request):
    """
    View all user's appointments.
    """
    appointments = Appointment.objects.filter(patient=request.user).select_related('doctor').order_by('-date')
    status_filter = request.GET.get('status')
    
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    context = {
        'appointments': appointments,
        'page_title': 'My Appointments',
        'selected_status': status_filter,
    }
    return render(request, 'doctors/my_appointments.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def write_review_view(request, doctor_id):
    """
    Write a review for a doctor.
    """
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    existing_review = Review.objects.filter(doctor=doctor, user=request.user).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            try:
                review = form.save(commit=False)
                review.doctor = doctor
                review.user = request.user
                review.save()
                
                message = '✅ Review updated successfully!' if existing_review else '✅ Review posted successfully!'
                messages.success(request, message)
                return redirect('search')
            except Exception as e:
                messages.error(request, f'❌ Error: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = ReviewForm(instance=existing_review)
    
    context = {
        'form': form,
        'doctor': doctor,
        'existing_review': existing_review,
        'page_title': f'Review Dr. {doctor.name}',
    }
    return render(request, 'doctors/write_review.html', context)


@login_required(login_url='login')
def my_reviews_view(request):
    """
    View all reviews written by the user.
    """
    reviews = Review.objects.filter(user=request.user).select_related('doctor').order_by('-created_at')
    
    context = {
        'reviews': reviews,
        'page_title': 'My Reviews',
    }
    return render(request, 'doctors/my_reviews.html', context)


# ==================== EXISTING VIEWS ====================

def search_doctors(request):
    """Search for doctors with filtering by name, location, and experience."""
    doctors = Doctor.objects.all()
    
    # Get search parameters from GET request
    name = request.GET.get('name', '')
    location = request.GET.get('location', '')
    min_experience = request.GET.get('min_experience', '')
    
    # Apply filters if parameters are provided
    if name:
        doctors = doctors.filter(name__icontains=name)
    
    if location:
        doctors = doctors.filter(location__icontains=location)
    
    if min_experience:
        try:
            min_exp_value = int(min_experience)
            doctors = doctors.filter(experience__gte=min_exp_value)
        except ValueError:
            pass
    
    context = {
        'doctors': doctors,
        'name': name,
        'location': location,
        'min_experience': min_experience,
    }
    
    return render(request, 'search.html', context)


@login_required(login_url='login')
@require_http_methods(["GET", "POST"])
def book_appointment(request, doctor_id=None):
    """Book an appointment with a doctor."""
    doctor = None
    
    # If doctor_id is provided, pre-select the doctor
    if doctor_id:
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            messages.error(request, "Doctor not found.")
            return redirect('search')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                # Save the form but don't commit to DB yet
                appointment = form.save(commit=False)
                # Set the patient to the logged-in user (already authenticated)
                appointment.patient = request.user
                # Now save to database
                appointment.save()
                messages.success(
                    request,
                    f"✅ Appointment booked successfully with Dr. {appointment.doctor.name} on {appointment.date}!"
                )
                return redirect('appointment_confirmation', appointment_id=appointment.id)
            except Exception as e:
                messages.error(request, f'❌ Error booking appointment: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        initial_data = {}
        if doctor:
            initial_data['doctor'] = doctor
        form = AppointmentForm(initial=initial_data)
    
    context = {
        'form': form,
        'doctor': doctor,
    }
    
    return render(request, 'book_appointment.html', context)


def appointment_confirmation(request, appointment_id):
    """Display appointment confirmation details."""
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found.")
        return redirect('search')
    
    context = {
        'appointment': appointment,
    }
    
    return render(request, 'confirmation.html', context)


# ==================== ML PREDICTION ====================

@require_http_methods(["GET", "POST"])
def predict_doctor_rating(request):
    """
    Predict doctor rating based on specialty and experience using ML model.
    """
    import pickle
    import os
    
    prediction = None
    error = None
    specialties_list = [
        ('anesthesiologist', 'Anesthesiologist'),
        ('ayurveda', 'Ayurveda'),
        ('cardiac-surgeon', 'Cardiac Surgeon'),
        ('cardiologist', 'Cardiologist'),
        ('dentist', 'Dentist'),
        ('dermatologist', 'Dermatologist'),
        ('endocrinologist', 'Endocrinologist'),
        ('gastroenterologist', 'Gastroenterologist'),
        ('general-physician', 'General Physician'),
        ('gynecologist', 'Gynecologist'),
        ('nephrologist', 'Nephrologist'),
        ('neurologist', 'Neurologist'),
        ('neurosurgeon', 'Neurosurgeon'),
        ('oncologist', 'Oncologist'),
        ('ophthalmologist', 'Ophthalmologist'),
        ('orthopedist', 'Orthopedist'),
        ('pathologist', 'Pathologist'),
        ('pediatrician', 'Pediatrician'),
        ('plastic-surgeon', 'Plastic Surgeon'),
        ('psychiatrist', 'Psychiatrist'),
        ('pulmonologist', 'Pulmonologist'),
        ('radiologist', 'Radiologist'),
        ('rheumatologist', 'Rheumatologist'),
        ('sexologist', 'Sexologist'),
        ('surgeon', 'Surgeon'),
        ('trichologist', 'Trichologist'),
        ('unani', 'Unani'),
        ('urologist', 'Urologist'),
        ('vascular-surgeon', 'Vascular Surgeon'),
    ]
    
    if request.method == 'POST':
        try:
            specialty = request.POST.get('specialty', '').strip()
            experience = request.POST.get('experience', '').strip()
            
            if not specialty or not experience:
                error = '❌ Please fill in all fields'
            else:
                try:
                    experience = int(experience)
                    if experience < 0 or experience > 70:
                        error = '❌ Experience should be between 0 and 70 years'
                    else:
                        # Load model and encoder
                        model_path = r'D:\Projects\Doctors Search website\models\model.pkl'
                        encoder_path = r'D:\Projects\Doctors Search website\models\encoder.pkl'
                        
                        if not os.path.exists(model_path) or not os.path.exists(encoder_path):
                            error = '❌ Model files not found. Please train the model first.'
                        else:
                            with open(model_path, 'rb') as f:
                                model = pickle.load(f)
                            with open(encoder_path, 'rb') as f:
                                encoder = pickle.load(f)
                            
                            # Encode specialty
                            try:
                                specialty_encoded = encoder.transform([specialty])[0]
                            except ValueError:
                                error = f'❌ Unknown specialty: {specialty}'
                                specialty_encoded = None
                            
                            if specialty_encoded is not None:
                                # Make prediction
                                predicted_rating = model.predict([[specialty_encoded, experience]])[0]
                                
                                # Ensure rating is between 1 and 5
                                predicted_rating = max(1.0, min(5.0, predicted_rating))
                                prediction = round(predicted_rating, 2)
                                messages.success(request, f'✅ Rating predicted: {prediction}')
                
                except ValueError:
                    error = '❌ Experience must be a valid number'
        except Exception as e:
            error = f'❌ Error: {str(e)}'
    
    context = {
        'prediction': prediction,
        'error': error,
        'specialties': specialties_list,
        'page_title': 'Predict Doctor Rating',
    }
    
    return render(request, 'doctors/predict.html', context)