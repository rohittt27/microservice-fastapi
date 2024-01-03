import logging
import os
from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from utils import mail_trigger
import threading
from dotenv import load_dotenv

load_dotenv('.env')


app = FastAPI()

class EmailSchema(BaseModel):
    email_to: str
    cc : Optional[str] = ""
    bcc : Optional[str] = ""
    subject: str
    template : str
    template_data: dict

@app.post("/send-email")
async def send_email(email: EmailSchema):
    try: 
        host = os.environ.get('EMAIL_HOST')
        host_email = os.environ.get('EMAIL_HOST_USER')
        host_password =os.environ.get('EMAIL_HOST_PASSWORD')
        port = os.environ.get('EMAIL_PORT')

        template = Template(email.template) # Create a Jinja2 Template object from the template HTML string

        rendered_template = template.render(email.template_data) # Render the template with the provided data

        body = rendered_template

        message = MIMEMultipart()
        message['From'] = host_email
        message['To'] = email.email_to
        message['Cc']= email.cc
        message['Bcc']= email.bcc
        message['Subject'] = email.subject
        message.attach(MIMEText(body, "html"))

        email_args = {
            'senderEmail':host_email,
            'port':port,
            'password':host_password,
            'body':body,
            'message':message,
            'server':host,
        }
            
        t = threading.Thread(target=mail_trigger, args=[email_args]) # thread to trigger 
        t.start()   
        
        return {"status_code":200, "data": "email sent"}
    except Exception as err:
        logging.error("Exception occurred while sending email- {}".format(err))
        return {"status_code":500, "data": str(err)}






