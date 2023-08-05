""" Dispatcher class file """


def json_check(json_object: dict, key_name: str, optional=False,
               from_type=None, is_function=None):
    """ Checks wether a json object-key respects some rules """
    value = json_object.get(key_name)
    name = str(json_object)
    if value is None:
        if optional:
            return value
        raise Exception(f'{name} missing key: {key_name}')

    ext_name = name + ': ' + key_name
    if from_type and not isinstance(value, from_type):
        raise Exception(f'{ext_name} wrong type: expected {str(from_type)}')
    if is_function and not callable(value):
        raise Exception(f'{ext_name} not a function')
    return value


class Dispatcher:
    """ Dispatchs function regarding user input """
    def __init__(self, config: dict):
        self.config = config
        self.check_config()

    def check_config(self):
        """ Check if config object is valid """
        config = self.config  # avoid repetition of self in "self.config"
        actions = json_check(config, 'actions', from_type=dict)
        for name, action in actions.items():
            # check that action is a dict
            json_check(actions, name, from_type=dict)
            # check action content
            json_check(action, 'pre-func', optional=True, is_function=True)
            json_check(action, 'func', is_function=True)
            json_check(action, 'post-func', optional=True, is_function=True)

    def execute_pre_func(self, user):
        """ Executes the pre-call of a handle """
        action = self.config['actions'][user.state]
        if callback := action.get('pre-func'):
            callback(user)

    def execute_func(self, user, user_input: str):
        """ Executes the call of a handle """
        self.config['actions'][user.state]['func'](user, user_input)

    def execute_post_func(self, user):
        """ Executes the post-call of a handle """
        action = self.config['actions'][user.state]
        if callback := action.get('post-func'):
            callback(user)
