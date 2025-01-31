from django.core.mail.backends.smtp import EmailBackend
import random

class CustomEmailBackend(EmailBackend):
    def __init__(self, *args, **kwargs):
        # Define multiple email configurations
        email_configs = [
            {
                'EMAIL_HOST_USER': '8b6088e8d8055d',
                'EMAIL_HOST_PASSWORD': '3eac09a4e694df',
            },
            {
                'EMAIL_HOST_USER': 'da55186b9ea8b7',
                'EMAIL_HOST_PASSWORD': '6938f349235fd8',
            }
        ]

        # Randomly select one of the email configurations
        selected_config = random.choice(email_configs)

        # Set the selected configuration
        kwargs['username'] = selected_config['EMAIL_HOST_USER']
        kwargs['password'] = selected_config['EMAIL_HOST_PASSWORD']

        super().__init__(*args, **kwargs)