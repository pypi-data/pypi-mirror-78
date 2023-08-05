""" FacebookMessenger class file"""
from pymessenger.bot import Bot as FbBot
from . import Messenger


class FacebookMessenger(Messenger):
    """ Implementation of the messenger class using facebooks backend """

    def __init__(self, authentication_token):
        self.authentication_token = authentication_token
        self.bot = FbBot(authentication_token)

    def send(self, user_id: str, text: str):
        """ Sends to the user_id (backend must understand) the text message"""
        self.bot.send_text_message(user_id, text)

    def mark_writing(self, user_id: str, write_on: bool):
        """ Sends the user the writing notification"""
        action = 'typing_on' if write_on else 'typing_off'
        self.bot.send_action(user_id, action)

    def mark_seen(self, user_id: str):
        """ Sends the user the writing notification"""
        self.bot.send_action(user_id, 'mark_seen')


def facebook_route(request, facebook_check_token, bot):
    """ Handles a facebook api messenger request """
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        token_resonse = request.args.get("hub.challenge")
        if token_sent == facebook_check_token:
            return token_resonse
        return 'Invalid token_check'
    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    message = message['message'].get('text')
                    if message:
                        return bot.user_handle(recipient_id, message)
    return "Message ignored"
