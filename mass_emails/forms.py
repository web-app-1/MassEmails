from django import forms

class EmailForm(forms.Form):
    # Configuración del correo
    email_host = forms.CharField(label="SMTP Server", max_length=100, initial='smtp.gmail.com')
    email_port = forms.IntegerField(label="SMTP Port", initial=587)
    email_address = forms.EmailField(label="Host Email")
    email_password = forms.CharField(label="App Password", widget=forms.PasswordInput)
    use_tls = forms.BooleanField(label="Use TLS", required=False, initial=True)
    use_ssl = forms.BooleanField(label="Use SSL", required=False, initial=False)
    
    # Detalles del mensaje
    subject = forms.CharField(max_length=100, label="About")
    message = forms.CharField(widget=forms.Textarea, label="Message")
    image = forms.ImageField(label="Image (optional)", required=False)
    contact_file = forms.FileField(label="Contacts File (txt)")
