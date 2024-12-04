import json
from django.shortcuts import render, redirect
from .forms import EmailForm
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import imghdr
import smtplib
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def home(request):
    return render(request, 'mass_emails/home.html')

def success(request):
    return render(request, 'mass_emails/success.html')

@login_required
def send_mass_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            # Extraer datos del formulario
            email_host = form.cleaned_data['email_host']
            email_port = int(form.cleaned_data['email_port'])
            email_address = form.cleaned_data['email_address']
            email_password = form.cleaned_data['email_password']
            use_tls = form.cleaned_data['use_tls']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            contact_file = form.cleaned_data['contact_file']

            # Leer archivo de contactos
            contacts = []
            for line in contact_file:
                email, name = line.decode().strip().split(', ')
                contacts.append({"email": email.strip(), "name": name.strip()})

            # Renderizar página de progreso con datos
            return render(
                request, 
                'mass_emails/progress.html', 
                {
                    "contacts": contacts,
                    "email_host": email_host,
                    "email_port": email_port,
                    "email_address": email_address,
                    "email_password": email_password,
                    "use_tls": use_tls,
                    "subject": subject,
                    "message": message,
                }
            )
    else:
        form = EmailForm()

    return render(request, 'mass_emails/send_email.html', {'form': form})

@login_required
def process_emails(request):
    if request.method == 'POST':
        try:
            contact = request.POST.get('contact')
            email_host = request.POST.get('email_host')
            email_port = int(request.POST.get('email_port'))
            email_address = request.POST.get('email_address')
            email_password = request.POST.get('email_password')
            use_tls = request.POST.get('use_tls') == 'True'
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            image_url = "https://i.imgur.com/IVtwyfD.jpeg"

            # Log para depuración
            print(f"Processing email for contact: {contact}")
            print(f"Email Host: {email_host}, Port: {email_port}")
            print(f"Use TLS: {use_tls}")

            if not contact:
                return JsonResponse({"status": "error", "message": "No contact provided"})

            email, name = contact.split(', ')
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = email_address
            msg['To'] = email

            html_content = f"""
                <html>
                    <body>
                        <h1>Hi, {name}!</h1>
                        <p>{message}</p>
                        <img src="{image_url}">
                    </body>
                    
                </html>
            """
            msg.attach(MIMEText(html_content, 'html'))

            # Configurar conexión SMTP
            server = smtplib.SMTP(email_host, email_port)
            if use_tls:
                server.starttls()
            server.login(email_address, email_password)
            server.sendmail(email_address, [email], msg.as_string())
            server.quit()

            return JsonResponse({"status": "success", "message": f"Email sent to {name} ({email})"})

        except Exception as e:
            print(f"Error: {e}")  # Log de error
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method"})


def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirigir al login después del logout