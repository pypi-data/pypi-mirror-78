""" ExtendedUser class file """


class ExtendedUser:
    """ Extends user with more capacities: redirects attr to user """
    def __init__(self, user, messenger, dispatcher, database):
        self.user = user
        self.messenger = messenger
        self.dispatcher = dispatcher
        self.database = database

    def send_message(self, message: str):
        """ Sends a message to the user(reprented by this object) """
        self.messenger.mark_writing(self.user.fb_id, True)
        self.messenger.send(self.user.fb_id, message)
        self.messenger.mark_writing(self.user.fb_id, False)

    def change_state(self, name: str):
        """ Changed a users state"""
        self.dispatcher.execute_post_func(self.user)
        self.user.state = name
        self.dispatcher.execute_pre_func(self.user)

    def init_state(self):
        """ Execute the necessary when a user first gets its state """
        self.dispatcher.execute_pre_func(self.user)

    def execute_handle(self, user_input: str):
        """ Executes the correct handle depending of the user.state """
        self.dispatcher.execute_func(self.user, user_input)
        self.dispatcher.execute_enter_func(self.user)

    def mark_seen(self):
        """ Marks the message as seen """
        self.messenger.mark_seen(self.user.fb_id)

    def get_argument(self, name, default=None):
        """ Query the argument of a user """
        Argument = self.database.argument_class
        res = self.user.arguments.filter(Argument.name == name).scalar()
        if res is None:
            return default
        return res.value

    def store_argument(self, name, value):
        """ Creates or replace Argument of user """
        Argument = self.database.argument_class
        argument = self.user.arguments.filter(Argument.name == name).scalar()
        if argument is None:
            self.user.arguments.append(
                argument := Argument(name=name, value=value))
        else:
            argument.value = value
        return argument
