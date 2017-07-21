from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def send_mail_alternatives(to, subject, html_content, text_content=None, from_email=None, reply_to=None):
    if text_content is None:
        text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_email, to, reply_to=reply_to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
