from twilio.rest import Client
from setting import  *

client = Client(ACCOUNT_SID, AUTH_TOKEN)
def send_message(message):
    if PHONE_ENABLE:
        client.messages.create(to = MY_PHONE, from_ = TWILIO_PHONE, body = message)
    else:
        pass