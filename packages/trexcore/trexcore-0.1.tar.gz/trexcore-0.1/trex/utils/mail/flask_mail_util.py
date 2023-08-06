'''
Created on 4 Jun 2020

@author: jacklok
'''

from flask_mail import Mail, Message 
import logging

def send_mail(receipient_list, subject, message, sender=None, app=None, is_html=False):
    msg = Message(subject, sender=sender, recipients=receipient_list)
    if is_html:
        msg.html = message
    else:
        msg.body = message
    
    mail = Mail(app=app)
    
    logging.debug('mail.username=%s', mail.username)
    logging.debug('mail.password=%s', mail.password)
        
    mail.send(msg)