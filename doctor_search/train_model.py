"""
Doctor Rating Prediction Model Training Script

This script trains a machine learning model to predict doctor ratings based on
specialty and years of experience. It uses Linear Regression and saves both
the trained model and the LabelEncoder for future predictions.

Requirements:
- pandas
- scikit-learn

Usage:
    python train_model.py
"""

import os
import pickle
import sys
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder


def get_csv_path():
    """
    Get the path to the CSV file using absolute path.
    
    Returns:
        str: Absolute path to the CSV file
    """
    # Use absolute path (works from any directory)
    csv_path = r"D:\Projects\Doctors Search website\bangalore_doctors_final.csv"
    return csv_path


def load_and_prepare_data(csv_file):
    """
    Load dataset and prepare it for model training.
    
    Args:
        csv_file (str): Path to the CSV file
        
    Returns:
        tuple: (dataframe with selected columns, cleaned dataframe)
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        KeyError: If required columns are missing
    """
    print(f"📂 Loading dataset from '{csv_file}'...")
    
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"❌ Dataset file not found: {csv_file}\n   Expected at: {os.path.abspath(csv_file)}")
    
    # Load CSV file
    df = pd.read_csv(csv_file)
    print(f"✅ Dataset loaded successfully! Shape: {df.shape}")
    
    # Select required columns
    required_columns = ['specialty', 'experience_years', 'rating']
    print(f"\n📋 Selecting columns: {required_columns}")
    
    try:
        df = df[required_columns]
    except KeyError as e:
        missing = set(required_columns) - set(df.columns)
        raise KeyError(f"❌ Missing required columns: {missing}") from e
    
    print(f"✅ Columns selected! Current shape: {df.shape}")
    
    # Check for missing values before dropping
    print(f"\n🔍 Checking for missing values...")
    missing_summary = df.isnull().sum()
    if missing_summary.sum() > 0:
        print("Missing values found:")
        for col, count in missing_summary[missing_summary > 0].items():
            print(f"  - {col}: {count} missing values")
        print("Dropping rows with missing values...")
        df = df.dropna()
        print(f"✅ Missing values removed! New shape: {df.shape}")
    else:
        print("✅ No missing values found!")
    
    return df


def encode_specialty(df):
    """
    Convert specialty (categorical) to numeric using LabelEncoder.
    
    Args:
        df (pd.DataFrame): DataFrame with specialty column
        
    Returns:
        tuple: (modified dataframe, fitted LabelEncoder)
    """
    print(f"\n🔤 Encoding 'specialty' column to numeric values...")
    
    encoder = LabelEncoder()
    df['specialty'] = encoder.fit_transform(df['specialty'])
    
    print(f"✅ Specialty encoded successfully!")
    print(f"   Unique specialties: {len(encoder.classes_)}")
    for idx, specialty in enumerate(encoder.classes_):
        print(f"   - {specialty} → {idx}")
    
    return df, encoder


def prepare_features_and_target(df):
    """
    Prepare input features (X) and target (y) for model training.
    
    Args:
        df (pd.DataFrame): Prepared dataframe
        
    Returns:
        tuple: (X features, y target)
    """
    print(f"\n🎯 Preparing features and target...")
    
    X = df[['specialty', 'experience_years']]
    y = df['rating']
    
    print(f"✅ Features prepared!")
    print(f"   Input features (X) shape: {X.shape}")
    print(f"   Target (y) shape: {y.shape}")
    print(f"   Feature columns: {list(X.columns)}")
    print(f"   Target column: rating")
    
    return X, y


def train_model(X, y):
    """
    Train Random Forest Regressor model for better accuracy.
    
    Args:
        X (pd.DataFrame): Input features
        y (pd.Series): Target values
        
    Returns:
        RandomForestRegressor: Trained model
    """
    print(f"\n🤖 Training Random Forest Regressor model...")
    
    model = RandomForestRegressor(
        n_estimators=100,      # 100 trees
        max_depth=15,          # Tree depth
        min_samples_split=5,   # Samples to split
        random_state=42,       # Reproducibility
        n_jobs=-1              # Use all CPU cores
    )
    model.fit(X, y)
    
    # Calculate training metrics
    train_score = model.score(X, y)
    
    print(f"✅ Model trained successfully!")
    print(f"   Model: Random Forest Regressor")
    print(f"   Trees: 100 | Max Depth: 15")
    print(f"   R² Score: {train_score:.4f}")
    print(f"   Feature Importance:")
    for idx, importance in enumerate(model.feature_importances_):
        feature_name = ['specialty', 'experience_years'][idx]
        print(f"   - {feature_name}: {importance:.4f}")
    
    return model


def save_model_and_encoder(model, encoder, model_file, encoder_file):
    """
    Save trained model and encoder to pickle files.
    
    Args:
        model (LinearRegression): Trained model
        encoder (LabelEncoder): Fitted encoder
        model_file (str): Path to save model
        encoder_file (str): Path to save encoder
    """
    print(f"\n💾 Saving model and encoder...")
    
    # Save model
    try:
        with open(model_file, 'wb') as f:
            pickle.dump(model, f)
        print(f"✅ Model saved as '{model_file}'")
        print(f"   File size: {os.path.getsize(model_file) / 1024:.2f} KB")
    except Exception as e:
        raise IOError(f"❌ Failed to save model: {e}") from e
    
    # Save encoder
    try:
        with open(encoder_file, 'wb') as f:
            pickle.dump(encoder, f)
        print(f"✅ Encoder saved as '{encoder_file}'")
        print(f"   File size: {os.path.getsize(encoder_file) / 1024:.2f} KB")
    except Exception as e:
        raise IOError(f"❌ Failed to save encoder: {e}") from e


def main():
    """Main execution function."""
    print("=" * 60)
    print("🏥 Doctor Rating Prediction Model Training")
    print("=" * 60)
    
    try:
        # Configuration - using absolute paths
        csv_file = get_csv_path()
        
        # Models directory (project root)
        models_dir = r"D:\Projects\Doctors Search website\models"
        os.makedirs(models_dir, exist_ok=True)
        
        model_file = os.path.join(models_dir, "model.pkl")
        encoder_file = os.path.join(models_dir, "encoder.pkl")
        
        # Step 1: Load and prepare data
        df = load_and_prepare_data(csv_file)
        
        # Step 2: Encode categorical data
        df, encoder = encode_specialty(df)
        
        # Step 3: Prepare features and target
        X, y = prepare_features_and_target(df)
        
        # Step 4: Train model
        model = train_model(X, y)
        
        # Step 5: Save model and encoder
        save_model_and_encoder(model, encoder, model_file, encoder_file)
        
        # Success message
        print("\n" + "=" * 60)
        print("✨ Model Training Completed Successfully!")
        print("=" * 60)
        print("\n📊 Summary:")
        print(f"  • Dataset: {csv_file}")
        print(f"  • Dataset found: Yes ✓")
        print(f"  • Rows used for training: {len(df)}")
        print(f"  • Model type: Linear Regression")
        print(f"  • Features: specialty, experience_years")
        print(f"  • Target: rating")
        print(f"  • Model saved: {model_file}")
        print(f"  • Encoder saved: {encoder_file}")
        print("\n💡 Next steps:")
        print(f"  1. Model files saved in: {models_dir}")
        print(f"  2. Use Django to make predictions")
        print(f"  3. Visit: http://localhost:8000/predict/")
        print("=" * 60 + "\n")
        
        return 0
    
    except FileNotFoundError as e:
        print(f"\n❌ Dataset file not found!")
        print(f"   Expected: {get_csv_path()}")
        print(f"   Error: {e}")
        print(f"\n💡 Solution: Ensure CSV file exists at the path shown above")
        return 1
    
    except KeyError as e:
        print(f"\n❌ Error: {e}")
        print(f"💡 Verify CSV has columns: specialty, experience_years, rating")
        return 1
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
