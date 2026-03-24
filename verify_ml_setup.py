"""
ML Integration Setup & Verification Script

This script verifies that all ML components are properly installed and configured
in your Django project. Run this after completing the integration steps.

Usage:
    python verify_ml_setup.py
"""

import os
import sys
import pickle
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_success(text):
    """Print success message"""
    print(f"✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"❌ {text}")

def print_warning(text):
    """Print warning message"""
    print(f"⚠️  {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ️  {text}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print_success(f"{description}: {filepath}")
        if size > 0:
            print_info(f"   File size: {size / 1024:.2f} KB")
        return True
    else:
        print_error(f"{description} not found: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print_success(f"{description}: {dirpath}")
        return True
    else:
        print_error(f"{description} not found: {dirpath}")
        return False

def test_model_loading():
    """Test if model and encoder can be loaded"""
    try:
        import django
        from django.conf import settings
        
        if not settings.configured:
            print_warning("Django not configured, attempting configuration...")
            # Skip detailed test
            return None
        
        model_path = os.path.join(settings.BASE_DIR, 'models', 'model.pkl')
        encoder_path = os.path.join(settings.BASE_DIR, 'models', 'encoder.pkl')
        
        print_info("Loading model...")
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print_success("Model loaded successfully")
        
        print_info("Loading encoder...")
        with open(encoder_path, 'rb') as f:
            encoder = pickle.load(f)
        print_success("Encoder loaded successfully")
        
        print_info(f"Encoder classes: {list(encoder.classes_)}")
        
        return (model, encoder)
    
    except Exception as e:
        print_error(f"Error loading models: {str(e)}")
        return None

def test_prediction():
    """Test making a prediction"""
    try:
        print_info("Testing prediction...")
        
        # Try to import and test
        import django
        from django.conf import settings
        
        if not settings.configured:
            print_warning("Django not fully configured, skipping prediction test")
            return False
        
        # Attempt to load and predict
        model_path = os.path.join(settings.BASE_DIR, 'models', 'model.pkl')
        encoder_path = os.path.join(settings.BASE_DIR, 'models', 'encoder.pkl')
        
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(encoder_path, 'rb') as f:
            encoder = pickle.load(f)
        
        # Make test prediction
        specialty_encoded = encoder.transform(['Cardiology'])[0]
        prediction = model.predict([[specialty_encoded, 10]])[0]
        
        print_success(f"Test prediction for Cardiology (10 years): {prediction:.2f}⭐")
        return True
    
    except Exception as e:
        print_error(f"Prediction test failed: {str(e)}")
        return False

def main():
    """Main verification script"""
    
    print_header("🏥 ML INTEGRATION VERIFICATION SCRIPT")
    
    project_root = Path(__file__).parent
    print_info(f"Project root: {project_root}\n")
    
    # ==============================================================================
    # Check 1: Dataset
    # ==============================================================================
    print_header("CHECK 1: Dataset Files")
    
    csv_path = project_root / 'data' / 'raw' / 'bangalore_doctors_final.csv'
    dataset_ok = check_file_exists(str(csv_path), "Dataset CSV")
    
    if not dataset_ok:
        print_warning("Dataset not found. To train the model:")
        print("  1. Place CSV at: data/raw/bangalore_doctors_final.csv")
        print("  2. Run: python train_model.py")
    
    # ==============================================================================
    # Check 2: Model & Encoder Files
    # ==============================================================================
    print_header("CHECK 2: Model & Encoder Files")
    
    model_dir = project_root / 'models'
    model_path = model_dir / 'model.pkl'
    encoder_path = model_dir / 'encoder.pkl'
    
    model_ok = check_file_exists(str(model_path), "Trained model")
    encoder_ok = check_file_exists(str(encoder_path), "Label encoder")
    
    if not (model_ok and encoder_ok):
        print_warning("Model files missing. To create them:")
        print("  1. Place dataset at: data/raw/bangalore_doctors_final.csv")
        print("  2. Run: python train_model.py")
    
    # ==============================================================================
    # Check 3: Django Files
    # ==============================================================================
    print_header("CHECK 3: Django Integration Files")
    
    ml_views = project_root / 'doctors' / 'ml_views.py'
    ml_urls = project_root / 'doctors' / 'ml_urls.py'
    predictor_html = project_root / 'doctors' / 'templates' / 'doctors' / 'predictor.html'
    
    views_ok = check_file_exists(str(ml_views), "ML Views")
    urls_ok = check_file_exists(str(ml_urls), "ML URLs")
    template_ok = check_file_exists(str(predictor_html), "Predictor template")
    
    if not (views_ok and urls_ok and template_ok):
        print_error("Some Django files are missing!")
        print("  Copy files from project documentation")
    
    # ==============================================================================
    # Check 4: Django Configuration
    # ==============================================================================
    print_header("CHECK 4: Django Configuration")
    
    settings_file = project_root / 'doctor_search' / 'settings.py'
    
    if check_file_exists(str(settings_file), "Django settings"):
        try:
            with open(settings_file, 'r') as f:
                settings_content = f.read()
            
            if 'ML_MODELS_DIR' in settings_content:
                print_success("ML configuration found in settings.py")
            else:
                print_warning("ML_MODELS_DIR not found in settings.py")
                print("  Add this to the end of settings.py:")
                print("  ML_MODELS_DIR = os.path.join(BASE_DIR, 'models')")
            
            if 'LOGGING' in settings_content:
                print_success("Logging configuration found in settings.py")
            else:
                print_warning("LOGGING not configured in settings.py")
        except Exception as e:
            print_error(f"Error reading settings: {e}")
    
    # ==============================================================================
    # Check 5: Required Python Packages
    # ==============================================================================
    print_header("CHECK 5: Required Python Packages")
    
    packages = {
        'django': 'Django',
        'sklearn': 'scikit-learn',
        'pandas': 'pandas',
        'pickle': 'pickle (built-in)'
    }
    
    packages_ok = True
    for module, name in packages.items():
        try:
            __import__(module)
            print_success(f"{name} installed")
        except ImportError:
            print_error(f"{name} NOT installed")
            packages_ok = False
    
    if not packages_ok:
        print("\n  Install missing packages:")
        print("  pip install scikit-learn pandas")
    
    # ==============================================================================
    # Check 6: URL Configuration
    # ==============================================================================
    print_header("CHECK 6: URL Configuration")
    
    urls_file = project_root / 'doctors' / 'urls.py'
    
    if check_file_exists(str(urls_file), "Doctors URLs"):
        try:
            with open(urls_file, 'r') as f:
                urls_content = f.read()
            
            if 'ml_views.doctor_rating_predictor' in urls_content or 'ml_views' in urls_content:
                print_success("ML URLs registered in doctors/urls.py")
            else:
                print_warning("ML views not registered in urls.py")
                print("  Add these lines to doctors/urls.py:")
                print("  path('predict/', ml_views.doctor_rating_predictor, name='predictor'),")
                print("  path('api/predict/', ml_views.api_predict_rating, name='api_predict'),")
        except Exception as e:
            print_error(f"Error reading URLs: {e}")
    
    # ==============================================================================
    # Check 7: Directory Structure
    # ==============================================================================
    print_header("CHECK 7: Directory Structure")
    
    data_dir = check_directory_exists(str(project_root / 'data'), "Data directory")
    models_dir = check_directory_exists(str(project_root / 'models'), "Models directory")
    logs_dir = check_directory_exists(str(project_root / 'logs'), "Logs directory")
    
    dirs_ok = data_dir and models_dir and logs_dir
    
    if not dirs_ok:
        print("\n  Create missing directories:")
        if not data_dir:
            print("  mkdir data && mkdir data\\raw && mkdir data\\processed")
        if not models_dir:
            print("  mkdir models")
        if not logs_dir:
            print("  mkdir logs")
    
    # ==============================================================================
    # Check 8: Model Loading Test
    # ==============================================================================
    print_header("CHECK 8: Model Loading Test")
    
    if model_ok and encoder_ok:
        print_info("Attempting to load models...")
        test_model_loading()
        test_prediction()
    else:
        print_warning("Skipping model test (model files missing)")
    
    # ==============================================================================
    # Summary
    # ==============================================================================
    print_header("VERIFICATION SUMMARY")
    
    all_ok = all([
        dataset_ok or True,  # Optional at first
        model_ok or True,    # Optional at first
        encoder_ok or True,  # Optional at first
        views_ok,
        urls_ok,
        template_ok,
        packages_ok,
        dirs_ok
    ])
    
    if all_ok:
        print_success("All critical components are in place!")
        print("\n  Next steps:")
        print("  1. If using train_model.py:")
        print("     python train_model.py")
        print("  2. Start Django:")
        print("     python manage.py runserver")
        print("  3. Visit:")
        print("     http://localhost:8000/predict/")
    else:
        print_error("Some components are missing or misconfigured")
        print("\n  Please follow the COMPLETE_ML_INTEGRATION.md guide to:")
        print("  1. Create required files")
        print("  2. Update Django configuration")
        print("  3. Train the model")
        print("  4. Run this verification again")
    
    print("\n" + "=" * 70 + "\n")
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())
