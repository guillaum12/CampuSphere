from django.core.mail import EmailMessage, get_connection, EmailMultiAlternatives
from convention import settings
from django.contrib import messages
from django.utils.html import strip_tags
from email.mime.image import MIMEImage


def send_email(request, subject, message, recipient_mail):
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
            # Créez l'email avec le sujet, le message HTML et le texte brut
            email = EmailMultiAlternatives(
                subject, 
                strip_tags(message), 
                email_from, 
                recipient_list, 
                connection=connection
            )
            email.attach_alternative(message, "text/html")
            
            # Attachez l'image avec un Content-ID
            with open('static/img/logo_complet.png', 'rb') as img:
                mime_image = MIMEImage(img.read())
                mime_image.add_header('Content-ID', '<logo>')
                mime_image.add_header('Content-Disposition', 'inline')
                email.attach(mime_image)
            
            # Envoyez l'email
            email.send()
    except Exception as e:
        print(e)
        messages.add_message(
            request,
            messages.ERROR,
            "Erreur lors de l'envoi de l'email : " + str(e),
        )