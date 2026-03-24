from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Doctor, Appointment, Review, UserProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'doctor', 'user', 'username', 'user_name', 'rating', 'title', 'comment', 'created_at', 'helpful_count']
        read_only_fields = ['id', 'user', 'created_at']
    
    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model"""
    
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'location', 'experience', 'contact', 'email', 'average_rating', 'total_reviews']
        read_only_fields = ['id', 'average_rating', 'total_reviews']


class DoctorDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Doctor model with reviews"""
    
    reviews = ReviewSerializer(many=True, read_only=True)
    appointment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'location', 'experience', 'contact', 'email', 
                  'bio', 'qualification', 'clinic_name', 'average_rating', 'total_reviews', 
                  'reviews', 'appointment_count', 'created_at']
        read_only_fields = ['id', 'average_rating', 'total_reviews', 'created_at']
    
    def get_appointment_count(self, obj):
        """Get total number of appointments for the doctor"""
        return obj.appointments.filter(status='completed').count()


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model"""
    
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    patient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'doctor_name', 'patient_name', 'date', 'time', 'status', 'notes', 'created_at']
        read_only_fields = ['id', 'patient', 'created_at']
    
    def get_patient_name(self, obj):
        return f"{obj.patient.first_name} {obj.patient.last_name}".strip() or obj.patient.username


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'phone', 'date_of_birth', 'address', 'city', 'state']
        read_only_fields = ['id']
