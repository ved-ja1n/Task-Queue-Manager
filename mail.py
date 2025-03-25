from email.message import EmailMessage
import ssl
import smtplib

context = ssl.create_default_context()

def send_gmail(sender, app_password, receivers, subject, body):
    em = EmailMessage()
    em['From'] = sender
    em['To'] = sender
    em['Subject'] = subject
    em.set_content(body)
    em['Bcc'] = ', '.join(receivers)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, app_password)
        smtp.sendmail(sender, receivers, em.as_string())