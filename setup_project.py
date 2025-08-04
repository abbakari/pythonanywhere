#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')

def run_migrations():
    """Run Django migrations"""
    print("🗄️ Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return False

def setup_django():
    """Setup Django environment"""
    try:
        django.setup()
        return True
    except Exception as e:
        print(f"❌ Error setting up Django: {e}")
        return False

def create_sample_data():
    """Create sample data for the application"""
    if not setup_django():
        return False
        
    # Import models after Django setup
    from django.contrib.auth.models import User
    from tickets.models import Ticket, Category, UserProfile, Budget
    
    print("🎯 Creating SUPERDOLL IT Help Desk sample data...")
    
    try:
        # Create categories
        categories = [
            'Hardware Issues',
            'Software Problems', 
            'Network Connectivity',
            'Email & Communication',
            'Security & Access',
            'Printer & Peripherals',
            'Database Issues',
            'System Performance'
        ]
        
        for cat_name in categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'description': f'Issues related to {cat_name.lower()}'}
            )
            if created:
                print(f"✅ Created category: {cat_name}")
        
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
        # Always set password to ensure it's correct
        admin_user.set_password('admin123')
        admin_user.email = 'admin@superdoll.com'
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save()
        
        if created:
            print("✅ Created admin user: admin@superdoll.com / admin123")
        else:
            print("✅ Updated admin user: admin@superdoll.com / admin123")
        
        # Create admin profile
        admin_profile, created = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={
                'is_admin': True,
                'department': 'IT Support',
                'phone': '+1-555-0100'
            }
        )
        admin_profile.is_admin = True
        admin_profile.save()
        
        # Create sample users
        users_data = [
            {'username': 'amali', 'email': 'abbakariamali@gmail.com', 'first_name': 'amali', 'last_name': 'abbak', 'dept': 'IT', 'office': 'IT Department'},
            {'username': 'billy', 'email': 'billy@gmail.com', 'first_name': 'billy', 'last_name': 'mashanda', 'dept': 'IT', 'office': 'IT Department'},
            {'username': 'kido', 'email': 'kido@gmail.com', 'first_name': 'kido', 'last_name': 'muhammed', 'dept': 'IT', 'office': 'IT Department'},
            {'username': 'said', 'email': 'said@gmail.com', 'first_name': 'said', 'last_name': 'muhammed', 'dept': 'IT', 'office': 'IT Department'},
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_active': True
                }
            )
            if created:
                user.set_password('user123')
                user.save()
                print(f"✅ Created user: {user_data['username']} / user123")
            
            # Create user profile
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'is_admin': False,
                    'department': user_data['dept'],
                    'office_name': user_data.get('office', 'Main Office'),
                    'phone': f'+1-555-{1000 + user.id:04d}'
                }
            )
        
        # Create sample tickets
        sample_tickets = [
            {
                'title': 'Computer won\'t start',
                'description': 'My workstation computer is not turning on. The power button doesn\'t respond and there are no lights or sounds when I press it. This started happening this morning.',
                'category': 'Hardware Issues',
                'priority': 'high',
                'user': 'amali'
            },
            {
                'title': 'Email not syncing',
                'description': 'Outlook is not receiving new emails since yesterday. I can send emails but nothing new is coming in. I\'ve tried restarting the application.',
                'category': 'Email & Communication',
                'priority': 'medium',
                'user': 'billy'
            },
            {
                'title': 'Printer offline',
                'description': 'The office printer shows as offline and won\'t print documents. The printer appears to be on and connected to the network.',
                'category': 'Printer & Peripherals',
                'priority': 'low',
                'user': 'amali'
            },
            {
                'title': 'Slow internet connection',
                'description': 'Internet speed is very slow, affecting productivity. Web pages take forever to load and file downloads are extremely slow.',
                'category': 'Network Connectivity',
                'priority': 'medium',
                'user': 'kido'
            },
            {
                'title': 'Software installation error',
                'description': 'Unable to install required software. Getting error message "Installation failed" every time I try to install the new accounting software.',
                'category': 'Software Problems',
                'priority': 'high',
                'user': 'said'
            }
        ]
        
        for ticket_data in sample_tickets:
            user = User.objects.get(username=ticket_data['user'])
            category = Category.objects.get(name=ticket_data['category'])
            
            ticket, created = Ticket.objects.get_or_create(
                title=ticket_data['title'],
                defaults={
                    'description': ticket_data['description'],
                    'category': category,
                    'priority': ticket_data['priority'],
                    'user': user,
                    'status': 'open'
                }
            )
            if created:
                print(f"✅ Created ticket: {ticket_data['title']}")
        
        # Create sample budgets
        budget_data = [
            {'name': 'Q1 Hardware Budget', 'amount': 50000, 'spent': 35000, 'category': 'Hardware Issues'},
            {'name': 'Software Licenses', 'amount': 25000, 'spent': 18000, 'category': 'Software Problems'},
            {'name': 'Network Infrastructure', 'amount': 30000, 'spent': 12000, 'category': 'Network Connectivity'},
        ]
        
        for budget_item in budget_data:
            try:
                category = Category.objects.get(name=budget_item['category'])
                budget, created = Budget.objects.get_or_create(
                    name=budget_item['name'],
                    defaults={
                        'amount': budget_item['amount'],
                        'spent': budget_item['spent'],
                        'category': category
                    }
                )
                if created:
                    print(f"✅ Created budget: {budget_item['name']}")
            except Category.DoesNotExist:
                print(f"⚠️ Category not found for budget: {budget_item['name']}")
        
        print("\n🎉 SUPERDOLL IT Help Desk setup complete!")
        print("🌐 Ready to launch at http://127.0.0.1:8000")
        print("\n🔐 Login Credentials:")
        print("👨‍💼 Admin: admin@superdoll.com / admin123 (click gear icon)")
        print("👤 Users: john_doe, jane_smith, mike_wilson, sarah_johnson / user123")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🚀 Setting up SUPERDOLL IT Help Desk System...")
    print("=" * 50)
    
    # Run migrations first
    if not run_migrations():
        print("❌ Failed to run migrations. Exiting.")
        sys.exit(1)
    
    # Create sample data
    if not create_sample_data():
        print("❌ Failed to create sample data. Exiting.")
        sys.exit(1)
    
    print("\n✅ Setup completed successfully!")
    print("🚀 You can now run: python manage.py runserver")
