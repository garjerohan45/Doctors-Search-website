#!/bin/bash
# Doctor Search System - Setup Script
# This script automates the setup of the Django application

echo "========================================="
echo "Doctor Search System - Setup Script"
echo "========================================="
echo ""

# Check Python installation
echo "✓ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✓ Python 3 found"
echo ""

# Create virtual environment
echo "✓ Creating virtual environment..."
python3 -m venv myvenv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "✓ Activating virtual environment..."
source myvenv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "✓ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Run migrations
echo "✓ Running database migrations..."
cd doctor_search
python manage.py makemigrations
python manage.py migrate
echo "✓ Database migrations completed"
echo ""

# Create superuser
echo "✓ Creating superuser..."
python manage.py createsuperuser
echo "✓ Superuser created"
echo ""

# Collect static files
echo "✓ Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected"
echo ""

# Display summary
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "To start the development server, run:"
echo "  cd doctor_search"
echo "  source ../myvenv/bin/activate  # On Windows: ..\myvenv\Scripts\activate"
echo "  python manage.py runserver"
echo ""
echo "Then visit:"
echo "  - Web: http://localhost:8000/"
echo "  - Admin: http://localhost:8000/admin/"
echo "  - API: http://localhost:8000/api/"
echo ""
echo "Documentation:"
echo "  - README.md - Getting started guide"
echo "  - API_DOCUMENTATION.md - REST API reference"
echo "  - PRODUCTION_GUIDE.md - Deployment guide"
echo "  - LIVE_SEARCH_GUIDE.md - Live search details"
echo ""
