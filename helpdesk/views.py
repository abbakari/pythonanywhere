from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from tickets.models import Ticket, TicketMessage
from django.contrib.auth.decorators import login_required

@login_required
@csrf_exempt
def check_notification(request):
    """
    Check for new notifications for the current user
    Returns JSON response with notification count and messages
    """
    user = request.user
    
    # Get unread messages for user's tickets
    unread_messages = TicketMessage.objects.filter(
        ticket__user=user,
        is_read=False
    ).exclude(
        user=user
    )
    
    # Get new tickets assigned to user (if admin)
    if user.is_staff:
        new_tickets = Ticket.objects.filter(
            assigned_to=user,
            status='open'
        )
    else:
        new_tickets = []
    
    # Prepare response data
    response_data = {
        'unread_messages': len(unread_messages),
        'new_tickets': len(new_tickets),
        'play_notification': False,
        'pending_count': 0
    }
    
    # Check if this is an admin request and if there are new notifications
    if user.is_staff and (len(unread_messages) > 0 or len(new_tickets) > 0):
        response_data['play_notification'] = True
        response_data['pending_count'] = len(unread_messages) + len(new_tickets)
    
    return JsonResponse(response_data)
