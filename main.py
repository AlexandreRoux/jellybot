from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
import requests
import random


app = Flask(__name__)

dict_words = \
    {'love': ['More than you imagine',
              'So much',
              'Yes my fish !',
              'Since the first day my love',
              'Let\'s get married tomorrow'],
     'other': []}

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if any(x in incoming_msg for x in ['like', 'love']):
        # return a reassure phrase
        msg.body(random.choice(dict_words['love']))
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)


if __name__ == '__main__':
    app.run()
