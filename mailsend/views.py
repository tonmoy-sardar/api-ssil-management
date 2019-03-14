from django.shortcuts import render
from mailsend.models import *

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template import Context,Template
# from mail.models import MailTemplate
from django.conf import settings



class GlobleMailSend(object):
    """docstring for GlobleMailSend"""
    def __init__(self, code, recipient_list:list):
        super(GlobleMailSend, self).__init__()
        self.code = code
        self.from_email = settings.EMAIL_FROM_C
        self.recipient_list = recipient_list

    def mailsend(self, mail_data:dict):
        print("self.code: ", self.code)
        mail_content = MailTemplate.objects.get(code = self.code)
        subject = mail_content.subject
        template_variable = mail_content.template_variable.split(",")
        html_content = Template(mail_content.html_content)
        match_data_dict = {}
        for data in template_variable:
            if data.strip() in mail_data:
                match_data_dict[data.strip()] = mail_data[data.strip()]

        if match_data_dict:
            context_data = Context(match_data_dict)
            
            html_content = html_content.render(context_data)

            msg = EmailMessage(subject, html_content, self.from_email, self.recipient_list)
            msg.content_subtype = "html"
            msg.send()
        print("mail send Done..... ")
        return True
        




