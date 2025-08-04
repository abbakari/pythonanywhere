from twilio.rest import Client
from django.conf import settings
from django.contrib.auth.models import User

def send_ticket_notification(ticket):
    """
    Send WhatsApp and SMS notification to admin about new ticket
    Args:
        ticket (Ticket): The newly created ticket instance
    Returns:
        bool: True if at least one notification was sent successfully, False otherwise
    """
    # Get all admin users
    try:
        admin_profiles = UserProfile.objects.filter(is_admin=True)
        if not admin_profiles.exists():
            print("No admin users found in the system")
            return False

        # Prepare message content
        message_content = f"""
        📝 New Ticket Created
        -------------------
        Title: {ticket.title}
        Created by: {ticket.user.username} ({ticket.user.email})
        Priority: {ticket.priority}
        Department: {ticket.user.userprofile.department}
        Office: {ticket.user.userprofile.office_name}
        """

        # Initialize Twilio client
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

        success = False
        
        # Send notifications to all admins
        for admin_profile in admin_profiles:
            try:
                # Send WhatsApp message
                whatsapp_message = client.messages.create(
                    from_=f'whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}',
                    to=f'whatsapp:{admin_profile.phone}',
                    body=message_content
                )

                # Send SMS message
                sms_message = client.messages.create(
                    from_=settings.TWILIO_WHATSAPP_NUMBER,
                    to=admin_profile.phone,
                    body=message_content
                )

                success = True

            except Exception as e:
                print(f"Error sending notification to {admin_profile.user.username}: {str(e)}")

        return success

    except Exception as e:
        print(f"Error in notification process: {str(e)}")
        return False
