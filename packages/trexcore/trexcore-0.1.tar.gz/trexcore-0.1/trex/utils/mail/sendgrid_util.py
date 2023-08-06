__author__ = 'jacklok'

from sendgrid.helpers.mail import To, From
import logging
from trex.conf import lib_conf

import sendgrid 
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail 
from six import string_types

SENDGRID_API_KEY = lib_conf.SENDGRID_API_KEY 
 
#sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

def send_email(sender=None, to_address=None, cc_address=None, bcc_address=None, subject=None, body=None, html=None, batch_id=None):
    logging.info('sender=%s', sender)
    logging.info('to_address=%s', to_address)
    logging.info('subject=%s', subject)
    logging.info('SENDGRID_API_KEY=%s', SENDGRID_API_KEY)

    if isinstance(to_address, string_types):
        to_address = (to_address)
    
    

    if html:
        message = Mail(
                    from_email          = sender,
                    to_emails           = to_address,
                    subject             = subject,
                    html_content        = html)
        
        
    elif body:
        message = Mail(
                    from_email          = sender,
                    to_emails           = to_address,
                    subject             = subject,
                    plain_text_content  = body)
        
        
    

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        logging.info('response.status_code=%s', response.status_code)
        logging.info('response.headers=%s', response.headers)
        logging.info('response.body=%s', response.body)

        return True
    except:
        raise











