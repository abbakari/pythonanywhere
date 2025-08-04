#!/bin/bash

echo "🚀 Setting up SUPERDOLL IT Help Desk System..."
echo "=============================================="

# Install dependencies
echo "📦 Installing dependencies..."
pip install django==4.2.7
pip install channels==4.0.0
pip install channels-redis==4.1.0
pip install django-cors-headers==4.3.1
pip install pillow==10.1.0
pip install python-decouple==3.8

# Create database and run migrations
echo "🗄️ Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Reset admin credentials to ensure they work
echo "🔧 Ensuring admin credentials are correct..."
python reset_admin_password.py

# Create superuser and sample data
echo "👤 Creating admin user and sample data..."
python setup_project.py

echo "✅ Setup complete!"
echo ""
echo "🎯 Starting SUPERDOLL IT Help Desk..."
echo "======================================"
echo "🌐 Server will be available at: http://127.0.0.1:8000"
echo "⏰ Loading screen duration: 6 seconds"
echo ""
echo "🔐 Login Credentials:"
echo "Admin (click gear icon): admin@superdoll.com / admin123"
echo "Users: john_doe, jane_smith, mike_wilson / user123"
echo ""
echo "🚀 Launching application..."

# Start the Django development server
python manage.py runserver
