from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile

def debug_admin_credentials(request):
    """Debug view to check admin credentials - REMOVE IN PRODUCTION"""
    try:
        admin_user = User.objects.get(username='admin')
        profile = admin_user.userprofile
        
        debug_info = {
            'username': admin_user.username,
            'email': admin_user.email,
            'is_staff': admin_user.is_staff,
            'is_superuser': admin_user.is_superuser,
            'is_admin_profile': profile.is_admin,
            'password_check': admin_user.check_password('admin123'),
            'profile_exists': True
        }
    except User.DoesNotExist:
        debug_info = {'error': 'Admin user does not exist'}
    except UserProfile.DoesNotExist:
        debug_info = {
            'username': admin_user.username,
            'email': admin_user.email,
            'error': 'Admin profile does not exist'
        }
    
    return JsonResponse(debug_info)
