""" DevMessenger class file"""
from . import Messenger


class DevMessenger(Messenger):
    """ Implementation of the messenger class using facebooks backend """

    def send(self, user_id: str, text: str):
        """ Sends to the user_id (backend must understand) the text message"""
        print(f'{user_id} > {text}')
