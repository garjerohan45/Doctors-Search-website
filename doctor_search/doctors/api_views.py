from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db.models import Avg
from .models import Doctor, Appointment, Review, UserProfile
from .serializers import (
    DoctorSerializer, DoctorDetailSerializer, AppointmentSerializer,
    ReviewSerializer, UserSerializer, UserRegistrationSerializer,
    UserProfileSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Pagination for API results"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    User registration endpoint
    POST /api/register/
    """
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Review model
    - GET /api/reviews/ - List all reviews
    - GET /api/reviews/<id>/ - Get specific review
    - POST /api/reviews/ - Create review (authenticated users only)
    - PUT/PATCH /api/reviews/<id>/ - Update review
    - DELETE /api/reviews/<id>/ - Delete review
    """
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['doctor', 'rating']
    permission_classes = [IsAuthenticated]
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Allow unauthenticated users to view reviews"""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        """Set the user and update doctor rating"""
        review = serializer.save(user=self.request.user)
        self.update_doctor_rating(review.doctor)
    
    def perform_destroy(self, instance):
        """Update doctor rating after deletion"""
        doctor = instance.doctor
        instance.delete()
        self.update_doctor_rating(doctor)
    
    @staticmethod
    def update_doctor_rating(doctor):
        """Calculate and update average rating for doctor"""
        avg_rating = doctor.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        doctor.average_rating = round(avg_rating, 1)
        doctor.total_reviews = doctor.reviews.count()
        doctor.save()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_helpful(self, request, pk=None):
        """Mark a review as helpful"""
        review = self.get_object()
        review.helpful_count += 1
        review.save()
        return Response({'helpful_count': review.helpful_count})


class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Doctor model providing:
    - GET /api/doctors/ - List all doctors with pagination and filtering
    - GET /api/doctors/<id>/ - Retrieve doctor by ID
    - POST /api/doctors/ - Create a new doctor
    - PUT /api/doctors/<id>/ - Update a doctor
    - DELETE /api/doctors/<id>/ - Delete a doctor
    - GET /api/doctors/search/ - Search doctors
    - GET /api/doctors/<id>/reviews/ - Get doctor's reviews
    """
    
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialization', 'location']
    search_fields = ['name', 'specialization', 'clinic_name']
    ordering_fields = ['name', 'experience', 'average_rating']
    ordering = ['-average_rating', 'name']
    
    def get_queryset(self):
        """Customize queryset based on query parameters"""
        queryset = Doctor.objects.all()
        
        # Filter by minimum experience
        min_experience = self.request.query_params.get('min_experience', None)
        if min_experience:
            try:
                queryset = queryset.filter(experience__gte=int(min_experience))
            except ValueError:
                pass
        
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return DoctorDetailSerializer
        return DoctorSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Custom search endpoint for doctors
        Query parameters:
        - name: Search by doctor name
        - specialization: Filter by specialization
        - location: Filter by location
        - min_experience: Filter by minimum years of experience
        """
        queryset = Doctor.objects.all()
        
        # Search by name
        name = request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        # Filter by specialization
        specialization = request.query_params.get('specialization', None)
        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)
        
        # Filter by location
        location = request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Filter by minimum experience
        min_experience = request.query_params.get('min_experience', None)
        if min_experience:
            try:
                min_exp_value = int(min_experience)
                queryset = queryset.filter(experience__gte=min_exp_value)
            except ValueError:
                return Response(
                    {'error': 'min_experience must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get reviews for a specific doctor"""
        doctor = self.get_object()
        reviews = doctor.reviews.all()
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        """Get completed appointments count for a doctor"""
        doctor = self.get_object()
        completed_appointments = doctor.appointments.filter(status='completed').count()
        return Response({'completed_appointments': completed_appointments})


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Appointment model
    - GET /api/appointments/ - List user's appointments
    - GET /api/appointments/<id>/ - Get appointment details
    - POST /api/appointments/ - Create appointment
    - PUT/PATCH /api/appointments/<id>/ - Update appointment
    - DELETE /api/appointments/<id>/ - Delete appointment
    """
    
    serializer_class = AppointmentSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['doctor', 'status', 'date']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only current user's appointments"""
        return Appointment.objects.filter(patient=self.request.user)
    
    def perform_create(self, serializer):
        """Set the patient to the current user"""
        serializer.save(patient=self.request.user)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for UserProfile model
    - GET /api/profile/ - Get current user's profile
    - PUT /api/profile/ - Update current user's profile
    """
    
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only current user's profile"""
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update current user's profile"""
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """
    ViewSet for Doctor model providing:
    - GET /api/doctors/ - List all doctors with pagination and filtering
    - GET /api/doctors/<id>/ - Retrieve doctor by ID
    - POST /api/doctors/ - Create a new doctor
    - PUT /api/doctors/<id>/ - Update a doctor
    - DELETE /api/doctors/<id>/ - Delete a doctor
    - GET /api/doctors/search/ - Search doctors by name, specialization, location, and experience
    """
    
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialization', 'location']
    search_fields = ['name', 'specialization']
    ordering_fields = ['name', 'experience']
    ordering = ['name']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return DoctorDetailSerializer
        return DoctorSerializer
    
    def get_queryset(self):
        """
        Customize queryset based on query parameters
        """
        queryset = Doctor.objects.all()
        
        # Filter by minimum experience
        min_experience = self.request.query_params.get('min_experience', None)
        if min_experience:
            try:
                queryset = queryset.filter(experience__gte=int(min_experience))
            except ValueError:
                pass
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Custom search endpoint for doctors with advanced filtering
        
        Query parameters:
        - name: Search by doctor name (case-insensitive)
        - specialization: Filter by specialization
        - location: Filter by location
        - min_experience: Filter by minimum years of experience
        
        Example: /api/doctors/search/?name=John&location=NYC&min_experience=5
        """
        
        queryset = Doctor.objects.all()
        
        # Search by name
        name = request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        # Filter by specialization
        specialization = request.query_params.get('specialization', None)
        if specialization:
            queryset = queryset.filter(specialization__icontains=specialization)
        
        # Filter by location
        location = request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Filter by minimum experience
        min_experience = request.query_params.get('min_experience', None)
        if min_experience:
            try:
                min_exp_value = int(min_experience)
                queryset = queryset.filter(experience__gte=min_exp_value)
            except ValueError:
                return Response(
                    {'error': 'min_experience must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        """
        Get all appointments for a specific doctor
        
        Example: /api/doctors/1/appointments/
        """
        doctor = self.get_object()
        appointments = doctor.appointment_set.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Appointment model providing:
    - GET /api/appointments/ - List all appointments
    - GET /api/appointments/<id>/ - Retrieve appointment by ID
    - POST /api/appointments/ - Create a new appointment
    - PUT /api/appointments/<id>/ - Update an appointment
    - DELETE /api/appointments/<id>/ - Delete an appointment
    """
    
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['doctor', 'date']
    ordering_fields = ['date', 'patient_name']
    ordering = ['-date']
