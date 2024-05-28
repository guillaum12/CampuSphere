from django.core.mail import EmailMessage, get_connection
from convention import settings
from django.contrib import messages

def send_email(request, subject, message, recipient_mail):
    
    print(settings.EMAIL_HOST_PASSWORD)
    try:
        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
        ) as connection:
            subject = "[CampuSphère] " + subject
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [
                recipient_mail,
            ]
            message = message
            EmailMessage(
                subject, message, email_from, recipient_list, connection=connection
            ).send()
    except Exception as e:
        print(e)
        messages.add_message(
            request,
            messages.ERROR,
            "Erreur lors de l'envoi de l'email : " + str(e),

        )