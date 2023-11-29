from apps.account.send_sms import sending_sms
from apps.account.send_mail import send_confirmation_email
from config.celery import app


@app.task()
def send_confirmation_email_task(email, code):
    send_confirmation_email(email, code)


@app.task()
def send_confirmation_sms_task(phone_number, activation_code):
    sending_sms(phone_number, activation_code)



