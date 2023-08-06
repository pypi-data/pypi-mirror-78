""" Messenger class file """


class Messenger:
    """ Class that represents a messenger object (interface) """

    def send(self, user_id: str, text: str):
        """ Sends to the user_id (backend must understand) the text message"""
        raise NotImplementedError("Abstract method MUST be implemented")

    def mark_writing(self, user_id: str, write_on: bool):
        """ Sends the user the writing notification"""
        # Does nothing if not supported

    def mark_seen(self, user_id: str):
        """ Sends the user the writing notification"""
        # Does nothing if not supported
