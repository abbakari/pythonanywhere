#!/usr/bin/env python
import os
import sys
import django
from django.contrib.auth.models import User
from tickets.models import UserProfile

def reset_admin_password():
    """Reset admin password and ensure profile exists"""
    print("🔧 Resetting admin credentials...")
    
    try:
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@superdoll.com',
                'first_name': 'System',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        # Set password and ensure all fields are correct
        admin_user.set_password('admin123')
        admin_user.email = 'admin@superdoll.com'
        admin_user.first_name = 'System'
        admin_user.last_name = 'Administrator'
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save()
        
        # Create or update admin profile
        admin_profile, profile_created = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={
                'is_admin': True,
                'department': 'IT Support',
                'phone': '+1-555-0100'
            }
        )
        
        # Ensure profile is admin
        admin_profile.is_admin = True
        admin_profile.department = 'IT Support'
        admin_profile.phone = '+1-555-0100'
        admin_profile.save()
        
        print("✅ Admin credentials reset successfully!")
        print("📧 Email: admin@superdoll.com")
        print("🔑 Password: admin123")
        print("👤 Username: admin")
        print("🛡️ Admin privileges: Enabled")
        print("📱 Department: IT Support")
        
        # Verify the setup
        print("\n🔍 Verifying setup...")
        test_user = User.objects.get(username='admin')
        test_profile = test_user.userprofile
        
        print(f"✓ User exists: {test_user.username}")
        print(f"✓ Email: {test_user.email}")
        print(f"✓ Is staff: {test_user.is_staff}")
        print(f"✓ Is superuser: {test_user.is_superuser}")
        print(f"✓ Is active: {test_user.is_active}")
        print(f"✓ Profile is admin: {test_profile.is_admin}")
        print(f"✓ Password check: {test_user.check_password('admin123')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error resetting admin credentials: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    # Add the current directory to Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')

    try:
        django.setup()
    except Exception as e:
        print(f"❌ Error setting up Django: {e}")
        print("Make sure you're running this from the project root directory.")
        sys.exit(1)

    reset_admin_password()
