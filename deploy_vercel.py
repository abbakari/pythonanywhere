#!/usr/bin/env python3
"""
Vercel Deployment Script for Django IT Helpdesk
Prepares the project for Vercel deployment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def main():
    """Main deployment preparation function"""
    print("🚀 Preparing Django IT Helpdesk for Vercel deployment...")
    
    # Set Django settings for Vercel
    os.environ['DJANGO_SETTINGS_MODULE'] = 'helpdesk.settings_vercel'
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the Django project root.")
        sys.exit(1)
    
    # Install requirements
    run_command('pip install -r requirements.txt', 'Installing requirements')
    
    # Create staticfiles directory
    staticfiles_dir = Path('staticfiles')
    staticfiles_build_dir = Path('staticfiles_build')
    
    if staticfiles_dir.exists():
        shutil.rmtree(staticfiles_dir)
    if staticfiles_build_dir.exists():
        shutil.rmtree(staticfiles_build_dir)
    
    # Collect static files
    run_command('python manage.py collectstatic --noinput --clear', 'Collecting static files')
    
    # Create staticfiles_build directory for Vercel
    staticfiles_build_dir.mkdir(exist_ok=True)
    if staticfiles_dir.exists():
        shutil.copytree(staticfiles_dir, staticfiles_build_dir / 'static', dirs_exist_ok=True)
    
    # Create cache table (if database is accessible)
    run_command('python manage.py createcachetable django_cache_table', 'Creating cache table')
    
    # Check deployment configuration
    run_command('python manage.py check --deploy', 'Checking deployment configuration')
    
    print("\n🎉 Vercel deployment preparation completed!")
    print("\n📋 Next steps:")
    print("1. Set up a cloud MySQL database (PlanetScale, Railway, or AWS RDS)")
    print("2. Update your database credentials in Vercel environment variables")
    print("3. Install Vercel CLI: npm i -g vercel")
    print("4. Login to Vercel: vercel login")
    print("5. Deploy: vercel --prod")
    print("\n💡 Don't forget to add all environment variables to your Vercel project!")

if __name__ == '__main__':
    main()
