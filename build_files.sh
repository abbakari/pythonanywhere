#!/bin/bash

# Build script for Vercel deployment
echo "🚀 Starting Vercel build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Set Django settings for Vercel
export DJANGO_SETTINGS_MODULE=helpdesk.settings_vercel

# Create cache table for database caching
echo "🗄️ Creating cache table..."
python manage.py createcachetable django_cache_table || echo "Cache table already exists or creation failed"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create staticfiles_build directory for Vercel
echo "📂 Preparing static files for Vercel..."
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/ 2>/dev/null || echo "No static files to copy"

# Run database migrations (if database is accessible)
echo "🔄 Running database migrations..."
python manage.py migrate --run-syncdb || echo "Migration failed or database not accessible during build"

echo "✅ Vercel build process completed!"
