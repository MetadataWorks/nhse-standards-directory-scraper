

# import smtplib, ssl

from decouple import config
from redmail import outlook



outlook.username = config('sender_email_id') 
outlook.password = config('sender_email_password')


def send_email_notification(receiver_list, message, subject="Changes found in NHS APIs data"):

    outlook.send(
        receivers=receiver_list,
        subject=subject,
        text=message
    )


