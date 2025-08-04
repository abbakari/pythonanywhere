"""
Production deployment script for Django IT Helpdesk.
This script handles common deployment tasks.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def deploy_production():
    """Deploy the application for production."""
    print("🚀 Starting production deployment...")
    
    # Set environment variable for production settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'helpdesk.settings_production'
    
    # Install production requirements
    if not run_command("pip install -r requirements_production.txt", "Installing production requirements"):
        return False
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        return False
    
    # Run database migrations
    if not run_command("python manage.py migrate", "Running database migrations"):
        return False
    
    # Create superuser (optional - will prompt)
    print("\n📝 You may want to create a superuser account:")
    print("Run: python manage.py createsuperuser")
    
    # Check deployment
    if not run_command("python manage.py check --deploy", "Checking deployment configuration"):
        print("⚠️  Deployment check found issues. Please review the output above.")
    
    print("\n🎉 Production deployment completed!")
    print("\n📋 Next steps:")
    print("1. Configure your web server (nginx/apache)")
    print("2. Set up SSL certificates")
    print("3. Configure your domain DNS")
    print("4. Set up monitoring and backups")
    print("5. Create a superuser: python manage.py createsuperuser")
    
    return True

if __name__ == "__main__":
    deploy_production()
