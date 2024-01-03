import smtplib
import logging

def mail_trigger(email_args):
    try:
        with smtplib.SMTP(email_args['server'], email_args['port']) as smtp:
            smtp.starttls()
            smtp.login(email_args['senderEmail'], email_args['password'])
            smtp.send_message(email_args['message'])
    except Exception as err:
        logging.error("Exception occurred while sending email- {}".format(err))
