# 🚀 Model Training - Ready to Execute

## Status
✅ **READY** - All paths configured and data in place

## Quick Start
Run the training script from anywhere:

```bash
cd d:\Projects\Doctors\ Search\ website
python doctor_search/train_model.py
```

Or from the doctor_search directory:

```bash
cd d:\Projects\Doctors\ Search\ website\doctor_search
python train_model.py
```

## What's Configured

### ✅ CSV Data File
- **Location**: `d:\Projects\Doctors Search website\bangalore_doctors_final.csv`
- **Status**: Created with 60 rows of sample data
- **Format**: specialty, experience_years, rating
- **Path Type**: Absolute (works from any location)

### ✅ Training Script
- **Location**: `d:\Projects\Doctors Search website\doctor_search\train_model.py`
- **Status**: Fully configured with absolute paths
- **CSV Path**: Hardcoded to project root
- **Output Dir**: Will create `models/` at project root

### ✅ Output Location
- **Directory**: `d:\Projects\Doctors Search website\models\`
- **Files Generated**:
  - `model.pkl` - Trained Linear Regression model
  - `encoder.pkl` - LabelEncoder for specializations

## Expected Output

When you run the script, you'll see:

```
============================================================
🏥 Doctor Rating Prediction Model Training
============================================================

✅ [...loading and processing messages...]

============================================================
✨ Model Training Completed Successfully!
============================================================

📊 Summary:
  • Dataset: d:\Projects\Doctors Search website\bangalore_doctors_final.csv
  • Dataset found: Yes ✓
  • Rows used for training: 60
  • Model type: Linear Regression
  • Features: specialty, experience_years
  • Target: rating
  • Model saved: d:\Projects\Doctors Search website\models\model.pkl
  • Encoder saved: d:\Projects\Doctors Search website\models\encoder.pkl

💡 Next steps:
  1. Model files saved in: d:\Projects\Doctors Search website\models
  2. Use Django to make predictions
  3. Visit: http://localhost:8000/predict/
============================================================
```

## Next Steps After Training

1. **Verify model files exist**:
   ```bash
   ls d:\Projects\Doctors\ Search\ website\models\
   ```
   Should see: `model.pkl` and `encoder.pkl`

2. **Start Django server**:
   ```bash
   python manage.py runserver
   ```

3. **Test predictions**:
   - Visit: `http://localhost:8000/predict/`
   - Select a specialization and enter years of experience
   - Should see predicted rating with details

4. **Test API**:
   ```bash
   curl -X POST http://localhost:8000/api/predict/ \
     -H "Content-Type: application/json" \
     -d '{"specialization": "Cardiology", "experience_years": 5}'
   ```

## Troubleshooting

If script fails:

1. **"CSV file not found"**
   - Verify: `d:\Projects\Doctors Search website\bangalore_doctors_final.csv` exists
   - File must have columns: specialty, experience_years, rating

2. **"Permission denied"**
   - Check folder permissions
   - Ensure models/ directory can be created

3. **"Module not found"**
   - Ensure virtual environment active
   - Run: `pip install pandas scikit-learn`

## Files Ready

- ✅ `train_model.py` - Script to run
- ✅ `bangalore_doctors_final.csv` - Training data (60 rows)
- ✅ `ml_views.py` - Django views for predictions
- ✅ `predictor.html` - Prediction form UI
- ✅ `ml_urls.py` - URL routing

**Everything is configured and ready to go! 🎯**
