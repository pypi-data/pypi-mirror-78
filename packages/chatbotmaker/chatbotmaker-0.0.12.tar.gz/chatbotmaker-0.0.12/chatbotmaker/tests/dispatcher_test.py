from ..dispatcher import json_check, Dispatcher, initialize_from_function_name
from . import pytest, Mock, patch


# Multiple read only variable usage (lambda avoids coverage miss detection)
func_welcome = lambda user, user_input: user_input
enter_func_welcome = lambda user, user_input: user_input
pre_func_welcome = lambda user, user_input: user_input
post_func_welcome = lambda user, user_input: user_input


@pytest.mark.parametrize('json,key', [
    ({}, 'data'),
    ({'nope': 42}, 'data'),
])
def test_json_invalid_missing(json, key):
    with pytest.raises(Exception) as exception_info:
        json_check(json, key)
    assert 'missing key' in str(exception_info)


@pytest.mark.parametrize('value,type', [
    ('value', int),
    (1, float),
    (1.2, list),
    ([1], dict),
    ({'a': 'b'}, str),
])
def test_json_invalid_type(value, type):
    json = {'data': value}
    with pytest.raises(Exception) as exception_info:
        json_check(json, 'data', from_type=type)
    assert 'wrong type' in str(exception_info)


def test_json_invalid_type_function():
    json = {'data': 'not_func'}
    with pytest.raises(Exception) as exception_info:
        json_check(json, 'data', is_function=True)
    assert 'not a function' in str(exception_info)


@pytest.mark.parametrize('json,key', [
    ({'hi': 'there'}, 'ho'),
    ({'hi': 'there'}, 'hi'),
])
def test_json_valid_optional(json, key):
    res = json_check(json, key, optional=True)
    assert res == json.get(key)


@pytest.mark.parametrize('json,key,error,args', [
    ({'hi': 'there'}, 'hi', 'wrong type', {'from_type': int}),
    ({'hi': 42}, 'hi', 'wrong type', {'from_type': str}),
])
def test_json_invalid_optional(json, key, error, args):
    with pytest.raises(Exception) as exception_info:
        json_check(json, key, optional=True, **args)
    assert error in str(exception_info)


def test_dispatcher_init():
    config = {
        'actions': {
            'home': {'func': lambda user, text: text}
        }
    }
    dispatcher = Dispatcher(config)
    assert dispatcher.config == config


def test_dispatcher_init_with_default():
    config = {
        'actions': {
            'welcome': Dispatcher.DEFAULT,
            'home': {'func': lambda user, text: text},
        }
    }
    # When
    dispatcher = Dispatcher(config, globals())
    # Then
    welcom_obj = dispatcher.config['actions']['welcome']
    assert callable(dispatcher.config['actions']['home']['func'])
    assert welcom_obj['pre_func'] == pre_func_welcome
    assert welcom_obj['func'] == func_welcome
    assert welcom_obj['post_func'] == post_func_welcome


@pytest.mark.parametrize('method_name, name, args', [
    ('execute_pre_func', 'pre_func', []),
    ('execute_post_func', 'post_func', []),
    ('execute_enter_func', 'enter_func', []),
    ('execute_func', 'func', ['user_input']),
])
def test_execute_event_wrappers(method_name, name, args):
    # Given
    user = Mock()
    dispatcher = Dispatcher({'actions': {}}, None)
    # When
    with patch.object(dispatcher, 'execute_event', Mock()):
        method = getattr(dispatcher, method_name)
        method(user, *args)
        dispatcher.execute_event.assert_called_once_with(user, name, *args)


@pytest.mark.parametrize('method_name, name, args', [
    ('execute_event', 'pre_func', []),
    ('execute_event', 'func', ['']),
])
def test_execute_events(method_name, name, args):
    # Given
    config = {
        'actions': {
            'home': {
                'func': Mock(),
                'pre_func': Mock(), }}}
    dispatcher = Dispatcher(config)
    user = Mock(state='home')
    # When
    method = getattr(dispatcher, method_name)
    method(user, name, *args)
    # Then
    config['actions']['home'][name].assert_called_once_with(user, *args)


def test_initialize_from_function_name_with_optionals():
    # When
    res = initialize_from_function_name('welcome', globals())
    # Then
    assert res.get('func') == func_welcome
    assert res.get('pre_func') == pre_func_welcome
    assert res.get('post_func') == post_func_welcome


def test_initialize_from_function_name_missing_mandatory():
    with pytest.raises(KeyError):
        res = initialize_from_function_name('welcome', locals())
