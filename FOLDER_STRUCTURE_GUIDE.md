# Django + ML Project Folder Structure Guide

This document outlines the recommended folder structure for a Django project that includes machine learning models.

---

## 📁 Recommended Project Structure

```
doctor_search/
│
├── 📂 ml_models/                          ← Machine Learning Module
│   ├── __init__.py
│   ├── train_model.py                     ← Model training script
│   ├── predict.py                         ← Prediction utilities
│   └── utils.py                           ← ML helper functions
│
├── 📂 data/                               ← Data Storage
│   ├── raw/                               ← Original/raw datasets
│   │   └── bangalore_doctors_final.csv    ← Raw dataset
│   ├── processed/                         ← Processed datasets
│   │   └── doctors_processed.csv
│   └── README.md                          ← Data documentation
│
├── 📂 models/                             ← Trained Models & Encoders
│   ├── model.pkl                          ← Trained Linear Regression
│   ├── encoder.pkl                        ← LabelEncoder for specialty
│   ├── README.md                          ← Model documentation
│   └── training_config.json               ← Training parameters
│
├── 📂 doctor_search/                      ← Django Main Project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── 📂 doctors/                            ← Django App
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── api_views.py
│   ├── urls.py
│   ├── serializers.py
│   ├── forms.py
│   ├── admin.py
│   ├── signals.py
│   └── apps.py
│
├── 📂 predictions/                        ← Optional: App for ML predictions
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── serializers.py
│   └── admin.py
│
├── 📂 logs/                               ← Application Logs
│   ├── training.log
│   └── predictions.log
│
├── 📂 myvenv/                             ← Virtual Environment
│   └── ...
│
├── 📄 manage.py
├── 📄 db.sqlite3
├── 📄 requirements.txt
├── 📄 .gitignore
├── 📄 README.md
├── 📄 train_model.py                      ← (Alternative location)
└── 📄 settings.json                       ← Configuration file
```

---

## 📋 Folder Descriptions

### 1. **`ml_models/`** - Machine Learning Module
Purpose: Centralized location for all ML-related code

**Contents:**
- `train_model.py` - Model training script
- `predict.py` - Prediction functions
- `utils.py` - Helper functions (preprocessing, validation)

**Advantages:**
- ✅ Separates ML logic from Django apps
- ✅ Reusable across multiple Django apps
- ✅ Easy to maintain and update
- ✅ Can be converted to package

**Usage:**
```python
# In Django view or API
from ml_models.predict import predict_rating
from ml_models.train_model import train_and_save_model
```

---

### 2. **`data/`** - Data Storage
Purpose: Organize datasets by stage

**Subfolders:**
- `raw/` - Original CSV files (never modify)
- `processed/` - Cleaned/processed datasets

**File Examples:**
- `data/raw/bangalore_doctors_final.csv` - Original dataset
- `data/processed/doctors_cleaned.csv` - After preprocessing
- `data/README.md` - Data documentation

**Best Practices:**
- ✅ Keep raw data untouched
- ✅ Never commit large CSV files (use .gitignore)
- ✅ Document data sources and schemas
- ✅ Use relative paths in scripts

**Sample .gitignore:**
```gitignore
data/raw/*.csv
data/processed/*.csv
```

---

### 3. **`models/`** - Trained Models & Artifacts
Purpose: Store serialized ML models and encoders

**Contents:**
- `model.pkl` - Trained Linear Regression model
- `encoder.pkl` - LabelEncoder for specialty
- `training_config.json` - Training parameters and metadata
- `README.md` - Model documentation

**File Structure Example:**
```json
{
  "model_type": "LinearRegression",
  "training_date": "2024-03-24",
  "training_samples": 500,
  "features": ["specialty", "experience_years"],
  "target": "rating",
  "r2_score": 0.8234,
  "metrics": {
    "mse": 0.245,
    "rmse": 0.495,
    "mae": 0.380
  }
}
```

**Usage:**
```python
import pickle
import json

# Load model
model = pickle.load(open('models/model.pkl', 'rb'))
encoder = pickle.load(open('models/encoder.pkl', 'rb'))

# Load metadata
with open('models/training_config.json') as f:
    config = json.load(f)
```

---

### 4. **`doctor_search/`** - Django Project Settings
Purpose: Main Django project configuration

**Contents:**
- `settings.py` - Configuration
- `urls.py` - URL routing
- `wsgi.py` - Production server
- `asgi.py` - Async server

**Stays unchanged** - No app-specific code here

---

### 5. **`doctors/`** - Main Django App
Purpose: Doctor search functionality

**Standard Django app structure:**
- Models, Views, URLs, Serializers, Forms, Admin

**Optional Enhancement - Add ML predictions:**
```python
# doctors/views.py
from ml_models.predict import predict_rating

def doctor_detail(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    predicted_rating = predict_rating(
        specialty=doctor.specialty,
        experience=doctor.experience_years
    )
    # Use predicted_rating in context
```

---

### 6. **`predictions/`** - Optional ML Predictions App
Purpose: Separate app for ML predictions (if needed)

**Use this if:**
- Predictions are complex or frequently updated
- Need separate API endpoints for predictions
- Want to track prediction history

**Example models:**
```python
class PredictionRequest(models.Model):
    specialty = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    predicted_rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prediction = models.ForeignKey(PredictionRequest, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)
```

---

### 7. **`logs/`** - Application Logs
Purpose: Store application and training logs

**Contents:**
- `training.log` - Model training progress and errors
- `predictions.log` - Prediction service logs
- `errors.log` - Application errors

**Usage:**
```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"Model trained with R² score: 0.8234")
logger.error(f"Prediction failed: {error_message}")
```

---

## 📍 File Location Decisions

### Where to place `train_model.py`?

| Location | Pros | Cons | When to Use |
|----------|------|------|-----------|
| `ml_models/` | ✅ Organized, reusable | - | **Recommended** - Most projects |
| `project_root/` | ✅ Easy to run | ❌ Clutters root | Small projects, one-off scripts |
| `management/commands/` | ✅ Django integration | ❌ Overkill | Django-heavy workflows |

**Recommendation:** Use `ml_models/train_model.py`

```bash
# Run from project root
python ml_models/train_model.py

# Or add to manage.py command:
python manage.py train_model
```

---

### Where to place the CSV dataset?

| Location | Pros | Cons | When to Use |
|----------|------|------|-----------|
| `data/raw/` | ✅ Organized, scalable | - | **Recommended** |
| `project_root/` | ✅ Easy access | ❌ Clutters root | Temporary |
| `Static files/` | ❌ Not recommended | ❌ Wrong location | Never |
| `Media files/` | ⚠️ Possible | ⚠️ Overkill | Large files served to users |

**Recommendation:** Use `data/raw/`.

```python
# Always use relative path
import os
csv_path = os.path.join('data', 'raw', 'bangalore_doctors_final.csv')

# Or better, from settings:
import django.conf
csv_path = os.path.join(django.conf.settings.BASE_DIR, 'data', 'raw', 'bangalore_doctors_final.csv')
```

---

### Where to place trained models?

| Location | Pros | Cons | When to Use |
|----------|------|------|-----------|
| `models/` | ✅ Dedicated folder, clear | - | **Recommended** |
| `project_root/` | ✅ Easy access | ❌ Clutters | Quick dev |
| `static/` | ❌ Not recommended | ❌ Wrong purpose | Never |
| `media/` | ⚠️ Possible | ⚠️ Not best practice | If served to users |
| Cloud (S3/GCS) | ✅ Scalable, versioned | ⚠️ Network overhead | Production |

**Recommendation:** Use `models/` locally, S3 in production.

---

## 🚀 Implementation Guide

### Step 1: Create Folder Structure
```bash
cd d:\Projects\Doctors\ Search\ website

# Create directories
mkdir ml_models data\raw data\processed models logs predictions

# Create __init__.py files
echo. > ml_models\__init__.py
echo. > predictions\__init__.py
```

### Step 2: Move Files
```bash
# Move training script
move train_model.py ml_models\

# Move dataset (if in root)
move bangalore_doctors_final.csv data\raw\

# Models go here after training
# model.pkl → models\
# encoder.pkl → models\
```

### Step 3: Update Python Paths
```python
# In train_model.py, update data loading:
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "data" / "raw" / "bangalore_doctors_final.csv"
MODEL_DIR = BASE_DIR / "models"

def load_data():
    df = pd.read_csv(CSV_FILE)
    return df

def save_model(model, encoder):
    pickle.dump(model, open(MODEL_DIR / "model.pkl", "wb"))
    pickle.dump(encoder, open(MODEL_DIR / "encoder.pkl", "wb"))
```

### Step 4: Update Django Settings
```python
# doctor_search/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ML Models configuration
ML_MODELS_DIR = os.path.join(BASE_DIR, 'models')
ML_DATA_DIR = os.path.join(BASE_DIR, 'data')
ML_LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Create directories if they don't exist
os.makedirs(ML_MODELS_DIR, exist_ok=True)
os.makedirs(ML_DATA_DIR, exist_ok=True)
os.makedirs(ML_LOG_DIR, exist_ok=True)

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(ML_LOG_DIR, 'app.log'),
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

### Step 5: Create .gitignore
```gitignore
# Data files (too large)
data/raw/*.csv
data/processed/*.csv
!data/README.md

# Model files (large, regeneratable)
models/*.pkl
models/*.joblib
!models/README.md
!models/training_config.json

# Logs
logs/*.log

# Python cache
__pycache__/
*.pyc
*.pyo
*.egg-info/

# Virtual environment
myvenv/
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Database
db.sqlite3

# Environment variables
.env
.env.local
```

---

## 📊 Complete Project Tree (Current State)

```
doctor_search/
├── ml_models/
│   ├── __init__.py
│   ├── train_model.py          ← Moved here
│   ├── predict.py              ← Create this
│   └── utils.py                ← Create this
├── data/
│   ├── raw/
│   │   └── bangalore_doctors_final.csv
│   ├── processed/
│   └── README.md
├── models/
│   ├── model.pkl               ← Generated after training
│   ├── encoder.pkl             ← Generated after training
│   ├── training_config.json
│   └── README.md
├── predictions/                ← Optional app
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
├── doctor_search/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── doctors/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── api_views.py
│   ├── serializers.py
│   ├── forms.py
│   ├── admin.py
│   ├── signals.py
│   ├── urls.py
│   └── apps.py
├── logs/
│   ├── training.log
│   ├── predictions.log
│   └── app.log
├── myvenv/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── .gitignore
├── settings.json
├── README.md
└── PRODUCTION_GUIDE.md

```

---

## 🎯 Quick Commands

```bash
# Run training script (from project root)
python ml_models/train_model.py

# Load model in Django shell
python manage.py shell
>>> import pickle
>>> from django.conf import settings
>>> model = pickle.load(open(settings.ML_MODELS_DIR + '/model.pkl', 'rb'))

# View logs
tail -f logs/training.log

# Check structure
tree doctor_search /A
```

---

## ✅ Checklist

- [ ] Create `ml_models/` directory
- [ ] Create `data/raw/` and `data/processed/` directories
- [ ] Create `models/` directory
- [ ] Move `train_model.py` to `ml_models/`
- [ ] Move CSV to `data/raw/`
- [ ] Create `logs/` directory
- [ ] Update `.gitignore` file
- [ ] Update `train_model.py` with new paths
- [ ] Update `settings.py` with ML configuration
- [ ] Create `ml_models/__init__.py`
- [ ] Create `data/README.md` with data documentation
- [ ] Create `models/README.md` with model documentation
- [ ] Test script runs correctly from new location

---

## 📚 Reference Documentation

For more details, see:
- [Django Project Layout](https://docs.djangoproject.com/en/stable/intro/reusable-apps/)
- [Python Packaging Guide](https://packaging.python.org/)
- [ML Project Structure Best Practices](https://cookiecutter-data-science.drivendata.org/)
