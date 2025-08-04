#!/usr/bin/env python
"""
Quick setup script for SUPERDOLL IT Help Desk
Run this if you're having issues with the other setup scripts
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 SUPERDOLL IT Help Desk - Quick Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ manage.py not found. Please run this script from the project root directory.")
        return False
    
    # Install dependencies
    dependencies = [
        'django==4.2.7',
        'channels==4.0.0',
        'channels-redis==4.1.0',
        'django-cors-headers==4.3.1',
        'pillow==10.1.0',
        'python-decouple==3.8'
    ]
    
    print("📦 Installing dependencies...")
    for dep in dependencies:
        if not run_command(f'pip install {dep}', f'Installing {dep}'):
            print(f"⚠️ Failed to install {dep}, but continuing...")
    
    # Run migrations
    if not run_command('python manage.py makemigrations', 'Creating migrations'):
        return False
    
    if not run_command('python manage.py migrate', 'Running migrations'):
        return False
    
    # Create superuser and sample data
    print("👤 Creating admin user and sample data...")
    try:
        # Import here to avoid Django setup issues
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
        import django
        django.setup()
        
        from django.contrib.auth.models import User
        from tickets.models import UserProfile, Category, Ticket, Budget
        
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@superdoll.com',
                'first_name': 'System',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()
        
        # Create admin profile
        admin_profile, _ = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={
                'is_admin': True,
                'department': 'IT Support',
                'phone': '+1-555-0100'
            }
        )
        admin_profile.is_admin = True
        admin_profile.save()
        
        # Create basic categories
        categories = ['Hardware Issues', 'Software Problems', 'Network Connectivity', 'Email & Communication']
        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name)
        
        print("✅ Admin user and basic data created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("🌐 You can now run: python manage.py runserver")
    print("\n🔐 Login Credentials:")
    print("👨‍💼 Admin: admin@superdoll.com / admin123")
    print("👤 Or username: admin / admin123")
    
    # Ask if user wants to start the server
    start_server = input("\n🚀 Start the development server now? (y/n): ").lower().strip()
    if start_server in ['y', 'yes']:
        print("🌐 Starting server at http://127.0.0.1:8000")
        os.system('python manage.py runserver')
    
    return True

if __name__ == '__main__':
    main()
