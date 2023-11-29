from django.core.mail import send_mail
from django.utils.html import format_html

def send_confirmation_email(email, code):
    activation_url = f'http://localhost:8000/api/v1/account/activate/?u={code}'
    message = format_html(
        'Здравствуйте, активируйте ваш аккаунт! Чтобы активировать аккаунт, перейдите по ссылке:<br><a href="{}">{}</a><br>Не передавайте этот код никому.',
        activation_url, activation_url)
    send_mail(
        "Здравствуйте, активируйте ваш аккаунт!",
        message,
        'shopapiviewadmin@gmail.com',
        [email],
        fail_silently=False,
    )
