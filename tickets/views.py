from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
import json
import csv
from django.views.decorators.csrf import csrf_exempt
from .notifications import send_ticket_notification

from .models import Ticket, Category, UserProfile, TicketMessage, Budget
from .forms import UserLoginForm, AdminLoginForm, TicketForm, TicketMessageForm, TicketUpdateForm


def landing_page(request):
    """Landing page with loading screen"""
    return render(request, 'tickets/landing.html')


def login_view(request):
    """Handle both user and admin login"""
    if request.method == 'POST':
        login_type = request.POST.get('login_type', 'user')
        
        if login_type == 'admin':
            email = request.POST.get('username')
            password = request.POST.get('password')
            
            try:
                users = User.objects.filter(email=email)
                if not users.exists():
                    messages.error(request, 'No user found with this email.')
                    return redirect('login')
                
                if users.count() > 1:
                    messages.error(request, 'Multiple accounts found with this email. Please contact support.')
                    return redirect('login')
                
                user = users.first()
                authenticated_user = authenticate(request, username=user.username, password=password)
                
                if authenticated_user:
                    try:
                        profile = authenticated_user.userprofile
                        if profile.is_admin:
                            login(request, authenticated_user)
                            
                            # Update all 'new' tickets to 'open' status
                            new_tickets = Ticket.objects.filter(status='new')
                            updated_count = new_tickets.update(status='open')
                            
                            pending_tickets = Ticket.objects.filter(status='open').count()
                            if pending_tickets > 0:
                                request.session['play_voice_notification'] = True
                                request.session['pending_tickets_count'] = pending_tickets
                            
                            if updated_count > 0:
                                messages.success(request, f"{updated_count} new tickets have been marked as open.")
                            return redirect('admin_dashboard')
                        else:
                            messages.error(request, 'You do not have admin privileges.')
                    except UserProfile.DoesNotExist:
                        messages.error(request, 'User profile not found.')
                else:
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                messages.error(request, 'No user found with this email address.')
        else:
            form = UserLoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                try:
                    user = User.objects.get(username=username)
                    login(request, user)
                    return redirect('user_dashboard')
                except User.DoesNotExist:
                    messages.error(request, 'Username not found.')
    
    return render(request, 'tickets/login.html')


@csrf_exempt
@login_required
def check_notification(request):
    """API endpoint to check if voice notification should play"""
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.is_admin:
        play_notification = request.session.pop('play_voice_notification', False)
        pending_count = request.session.pop('pending_tickets_count', 0)
        return JsonResponse({
            'play_notification': play_notification,
            'pending_count': pending_count,
            'message': f"You have {pending_count} new ticket{'s' if pending_count != 1 else ''} waiting for review."
        })
    return JsonResponse({'play_notification': False})


@login_required
def user_dashboard(request):
    """User dashboard shows all user's tickets regardless of archive status"""
    user_tickets = Ticket.objects.filter(user=request.user)
    
    stats = {
        'total_tickets': user_tickets.count(),
        'new_tickets': user_tickets.filter(status='new').count(),
        'open_tickets': user_tickets.filter(status='open').count(),
        'in_progress_tickets': user_tickets.filter(status='in_progress').count(),
        'resolved_tickets': user_tickets.filter(status='resolved').count(),
        'unresolved_tickets': user_tickets.filter(status='unresolved').count(),
    }
    
    recent_tickets = user_tickets.order_by('-created_at')[:5]
    
    context = {
        'stats': stats,
        'recent_tickets': recent_tickets,
        'user': request.user
    }
    
    return render(request, 'tickets/user_dashboard.html', context)


@login_required
def admin_dashboard(request):
    """Main admin dashboard"""
    if not request.user.userprofile.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('user_dashboard')

    # Get all tickets (including archived) for total count
    all_tickets = Ticket.objects.all()
    total_tickets = all_tickets.count()
    
    # Get non-archived tickets for active sections
    active_tickets = Ticket.objects.filter(is_archived=False)
    
    # Calculate status counts for all tickets (including archived)
    status_counts = {
        'new': all_tickets.filter(status='new').count(),
        'open': all_tickets.filter(status='open').count(),
        'in_progress': all_tickets.filter(status='in_progress').count(),
        'resolved': all_tickets.filter(status='resolved').count(),
        'unresolved': all_tickets.filter(status='unresolved').count(),
    }
    
    # Get recent tickets (non-archived)
    recent_tickets = active_tickets.order_by('-created_at')[:10]

    # Get priority statistics (including archived)
    priority_stats = {
        'urgent': {
            'total': all_tickets.filter(priority='urgent').count(),
            'new': all_tickets.filter(priority='urgent', status='new').count(),
            'open': all_tickets.filter(priority='urgent', status='open').count(),
            'in_progress': all_tickets.filter(priority='urgent', status='in_progress').count(),
            'resolved': all_tickets.filter(priority='urgent', status='resolved').count(),
            'unresolved': all_tickets.filter(priority='urgent', status='unresolved').count()
        },
        'high': {
            'total': all_tickets.filter(priority='high').count(),
            'new': all_tickets.filter(priority='high', status='new').count(),
            'open': all_tickets.filter(priority='high', status='open').count(),
            'in_progress': all_tickets.filter(priority='high', status='in_progress').count(),
            'resolved': all_tickets.filter(priority='high', status='resolved').count(),
            'unresolved': all_tickets.filter(priority='high', status='unresolved').count()
        },
        'medium': {
            'total': all_tickets.filter(priority='medium').count(),
            'new': all_tickets.filter(priority='medium', status='new').count(),
            'open': all_tickets.filter(priority='medium', status='open').count(),
            'in_progress': all_tickets.filter(priority='medium', status='in_progress').count(),
            'resolved': all_tickets.filter(priority='medium', status='resolved').count(),
            'unresolved': all_tickets.filter(priority='medium', status='unresolved').count()
        },
        'low': {
            'total': all_tickets.filter(priority='low').count(),
            'new': all_tickets.filter(priority='low', status='new').count(),
            'open': all_tickets.filter(priority='low', status='open').count(),
            'in_progress': all_tickets.filter(priority='low', status='in_progress').count(),
            'resolved': all_tickets.filter(priority='low', status='resolved').count(),
            'unresolved': all_tickets.filter(priority='low', status='unresolved').count()
        }
    }

    # Get category statistics (non-archived)
    category_stats = Category.objects.annotate(
        total_tickets=Count('tickets', filter=Q(tickets__is_archived=False)),
        new_tickets=Count('tickets', filter=Q(tickets__status='new', tickets__is_archived=False)),
        open_tickets=Count('tickets', filter=Q(tickets__status='open', tickets__is_archived=False)),
        in_progress_tickets=Count('tickets', filter=Q(tickets__status='in_progress', tickets__is_archived=False)),
        resolved_tickets=Count('tickets', filter=Q(tickets__status='resolved', tickets__is_archived=False)),
        unresolved_tickets=Count('tickets', filter=Q(tickets__status='unresolved', tickets__is_archived=False))
    ).order_by('-total_tickets')

    # Get monthly ticket data (non-archived)
    today = timezone.now().date()
    monthly_data = []
    for i in range(12):
        date = today.replace(day=1) - timedelta(days=30*i)
        month_tickets = active_tickets.filter(
            created_at__year=date.year,
            created_at__month=date.month
        ).count()
        monthly_data.append({
            'month': date.strftime('%B %Y'),
            'count': month_tickets
        })
    monthly_data.reverse()

    context = {
        'total_tickets': total_tickets,
        'open_tickets': status_counts['open'],
        'in_progress_tickets': status_counts['in_progress'],
        'resolved_tickets': status_counts['resolved'],
        'unresolved_tickets': status_counts['unresolved'],
        'new_tickets': status_counts['new'],
        'recent_tickets': recent_tickets,
        'priority_stats': priority_stats,
        'category_stats': category_stats,
        'monthly_data': json.dumps(monthly_data)
    }

    return render(request, 'tickets/admin_dashboard.html', context)


@login_required
def ticket_list(request):
    """Show all tickets (never filtered by archive status)"""
    is_admin = hasattr(request.user, 'userprofile') and request.user.userprofile.is_admin
    
    if is_admin:
        # Admin sees all tickets (including archived)
        tickets = Ticket.objects.select_related('user', 'category', 'assigned_to')
    else:
        # Users see all their tickets (including archived)
        tickets = Ticket.objects.filter(user=request.user).select_related('category')
    
    # Filtering options
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    category_filter = request.GET.get('category')
    
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)
    if category_filter:
        tickets = tickets.filter(category_id=category_filter)
    
    categories = Category.objects.all()
    
    context = {
        'tickets': tickets.order_by('-created_at'),
        'categories': categories,
        'is_admin': is_admin,
        'current_status': status_filter,
        'current_priority': priority_filter,
        'current_category': category_filter,
    }
    
    return render(request, 'tickets/ticket_list.html', context)


@login_required
def archive_resolved_tickets(request):
    """Archive resolved/unresolved tickets (only affects admin dashboard)"""
    if not request.user.userprofile.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('login')
    
    if request.method == 'POST':
        # Archive only resolved and unresolved tickets
        tickets_to_archive = Ticket.objects.filter(
            status__in=['resolved', 'unresolved'],
            is_archived=False
        )
        archived_count = tickets_to_archive.count()
        tickets_to_archive.update(is_archived=True)
        
        messages.success(request, f'{archived_count} tickets archived. They will no longer appear in dashboard statistics.')
        return redirect('admin_dashboard')
    
    # Show confirmation
    ticket_count = Ticket.objects.filter(
        status__in=['resolved', 'unresolved'],
        is_archived=False
    ).count()
    
    return render(request, 'tickets/confirm_archive.html', {
        'ticket_count': ticket_count,
        'message': 'This will archive resolved/unresolved tickets. They will remain visible in ticket lists but be removed from dashboard statistics.'
    })


@login_required
def view_archived_tickets(request):
    """View archived resolved/unresolved tickets (admin only)"""
    if not request.user.userprofile.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('login')
    
    archived_tickets = Ticket.objects.filter(
        is_archived=True,
        status__in=['resolved', 'unresolved']
    ).order_by('-resolved_at')
    
    return render(request, 'tickets/archived_tickets.html', {
        'tickets': archived_tickets
    })


@login_required
def create_ticket(request):
    """Create a new ticket with status 'new'"""
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.status = 'new'
            ticket.save()
            
            if send_ticket_notification(ticket):
                messages.success(request, 'Ticket created successfully! Admin has been notified.')
            else:
                messages.success(request, 'Ticket created successfully! Admin notification failed.')
            
            return redirect('ticket_list')
    else:
        form = TicketForm()
    
    return render(request, 'tickets/create_ticket.html', {'form': form})


@login_required
def ticket_detail(request, ticket_id):
    """View and manage individual ticket"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    is_admin = hasattr(request.user, 'userprofile') and request.user.userprofile.is_admin
    is_superuser = request.user.is_superuser
    
    # Permission check
    if not is_admin and ticket.user != request.user:
        messages.error(request, 'You can only view your own tickets.')
        return redirect('user_dashboard')
    
    # Auto status updates for admin
    if is_admin:
        if ticket.status == 'new':
            ticket.status = 'open'
            messages.info(request, 'Ticket status updated to Open.')
        elif ticket.status == 'open':
            ticket.status = 'in_progress'
            messages.info(request, 'Ticket status updated to In Progress.')
        ticket.save()
    
    # Forms
    message_form = TicketMessageForm()
    update_form = TicketUpdateForm(instance=ticket) if is_admin else None
    
    if request.method == 'POST':
        if 'message_submit' in request.POST:
            message_form = TicketMessageForm(request.POST)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.ticket = ticket
                message.user = request.user
                message.save()
                messages.success(request, 'Message added!')
                return redirect('ticket_detail', ticket_id=ticket.id)
        
        elif 'update_ticket' in request.POST and is_admin:
            if not is_superuser and request.POST.get('assigned_to'):
                messages.error(request, 'Only superadmins can assign tickets.')
                return redirect('ticket_detail', ticket_id=ticket.id)
            
            update_form = TicketUpdateForm(request.POST, instance=ticket)
            if update_form.is_valid():
                update_form.save()
                messages.success(request, 'Ticket updated!')
                return redirect('ticket_detail', ticket_id=ticket.id)
    
    ticket_messages = TicketMessage.objects.filter(ticket=ticket).select_related('user').order_by('created_at')
    
    context = {
        'ticket': ticket,
        'ticket_messages': ticket_messages,
        'is_admin': is_admin,
        'update_form': update_form,
        'message_form': message_form,
        'categories': Category.objects.all()
    }
    
    return render(request, 'tickets/ticket_detail.html', context)


@login_required
def export_tickets(request):
    """Export all tickets to CSV"""
    if not request.user.userprofile.is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('admin_dashboard')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tickets_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'User', 'Category', 'Status', 'Priority', 'Created', 'Resolved', 'Archived'])
    
    tickets = Ticket.objects.select_related('user', 'category').all()
    for ticket in tickets:
        writer.writerow([
            ticket.id,
            ticket.title,
            ticket.user.username,
            ticket.category.name if ticket.category else 'None',
            ticket.get_status_display(),
            ticket.get_priority_display(),
            ticket.created_at.strftime('%Y-%m-%d %H:%M'),
            ticket.resolved_at.strftime('%Y-%m-%d %H:%M') if ticket.resolved_at else 'Not resolved',
            'Yes' if ticket.is_archived else 'No'
        ])
    
    return response


@login_required
def api_ticket_stats(request):
    """API endpoint for dashboard statistics (non-archived only)"""
    try:
        if not request.user.userprofile.is_admin:
            return JsonResponse({'error': 'Access denied'}, status=403)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User profile not found'}, status=403)
    
    stats = {
        'total_tickets': Ticket.objects.filter(is_archived=False).count(),
        'new_tickets': Ticket.objects.filter(status='new', is_archived=False).count(),
        'open_tickets': Ticket.objects.filter(status='open', is_archived=False).count(),
        'in_progress_tickets': Ticket.objects.filter(status='in_progress', is_archived=False).count(),
        'resolved_tickets': Ticket.objects.filter(status='resolved', is_archived=False).count(),
        'high_priority': Ticket.objects.filter(priority='high', is_archived=False).count(),
        'urgent_priority': Ticket.objects.filter(priority='urgent', is_archived=False).count(),
    }
    
    category_data = list(Category.objects.annotate(
        ticket_count=Count('tickets', filter=Q(tickets__is_archived=False))
    ).values('name', 'ticket_count'))
    
    priority_data = []
    for priority in ['low', 'medium', 'high', 'urgent']:
        count = Ticket.objects.filter(priority=priority, is_archived=False).count()
        priority_data.append({'priority': priority.capitalize(), 'count': count})
    
    return JsonResponse({
        'stats': stats,
        'category_data': category_data,
        'priority_data': priority_data
    })


def logout_view(request):
    """Handle logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('landing')