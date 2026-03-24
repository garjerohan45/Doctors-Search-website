import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctor_search.settings')
django.setup()

from doctors.models import Doctor

# Sample doctors data
doctors_data = [
    {
        'name': 'Dr. Rahul Sharma',
        'specialization': 'cardiology',
        'location': 'Mumbai',
        'experience': 15,
        'email': 'rahul.sharma@clinic.com',
        'contact': '9876543210',
        'bio': 'Experienced cardiologist with 15 years of practice',
        'qualification': 'MBBS, MD Cardiology',
        'clinic_name': 'Heart Care Clinic'
    },
    {
        'name': 'Dr. Priya Patel',
        'specialization': 'dermatology',
        'location': 'Bangalore',
        'experience': 10,
        'email': 'priya.patel@clinic.com',
        'contact': '9876543211',
        'bio': 'Specialist in skin and cosmetic treatments',
        'qualification': 'MBBS, MD Dermatology',
        'clinic_name': 'Skin Wellness Center'
    },
    {
        'name': 'Dr. Amit Kumar',
        'specialization': 'orthopedics',
        'location': 'Delhi',
        'experience': 12,
        'email': 'amit.kumar@clinic.com',
        'contact': '9876543212',
        'bio': 'Expert in joint and bone disorders',
        'qualification': 'MBBS, MS Orthopedics',
        'clinic_name': 'Bone & Joint Hospital'
    },
    {
        'name': 'Dr. Neha Singh',
        'specialization': 'pediatrics',
        'location': 'Pune',
        'experience': 8,
        'email': 'neha.singh@clinic.com',
        'contact': '9876543213',
        'bio': 'Caring pediatrician for children health',
        'qualification': 'MBBS, MD Pediatrics',
        'clinic_name': 'Little Stars Clinic'
    },
    {
        'name': 'Dr. Rajesh Gupta',
        'specialization': 'neurology',
        'location': 'Chennai',
        'experience': 18,
        'email': 'rajesh.gupta@clinic.com',
        'contact': '9876543214',
        'bio': 'Senior neurologist with expertise in brain disorders',
        'qualification': 'MBBS, MD Neurology, DM',
        'clinic_name': 'Neuro Care Institute'
    },
    {
        'name': 'Dr. Anjali Verma',
        'specialization': 'gynecology',
        'location': 'Hyderabad',
        'experience': 11,
        'email': 'anjali.verma@clinic.com',
        'contact': '9876543215',
        'bio': 'Women health specialist',
        'qualification': 'MBBS, MD Obstetrics & Gynecology',
        'clinic_name': 'Womens Health Clinic'
    },
    {
        'name': 'Dr. Vikram Malhotra',
        'specialization': 'general_practice',
        'location': 'Kolkata',
        'experience': 20,
        'email': 'vikram.malhotra@clinic.com',
        'contact': '9876543216',
        'bio': 'General practitioner with comprehensive medical knowledge',
        'qualification': 'MBBS',
        'clinic_name': 'City Medical Center'
    },
    {
        'name': 'Dr. Seema Joshi',
        'specialization': 'dentistry',
        'location': 'Ahmedabad',
        'experience': 9,
        'email': 'seema.joshi@clinic.com',
        'contact': '9876543217',
        'bio': 'Expert in dental care and cosmetic dentistry',
        'qualification': 'BDS, MDS',
        'clinic_name': 'Smile Dental Clinic'
    }
]

# Create doctors
for doc in doctors_data:
    Doctor.objects.create(**doc)

print(f"✅ Successfully created {Doctor.objects.count()} sample doctors!")
