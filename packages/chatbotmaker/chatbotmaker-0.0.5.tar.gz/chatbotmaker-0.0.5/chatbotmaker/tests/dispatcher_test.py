from ..dispatcher import json_check, Dispatcher
from . import pytest, Mock


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


def test_execute_pre_func_exists():
    # Given
    def func(user):
        user.state = 'new_state'
    config = {
        'actions': {
            'home': {
                'func': lambda user, text: text, 'pre-func': func, }}}
    dispatcher = Dispatcher(config)
    user = Mock(state='home')
    # When
    dispatcher.execute_pre_func(user)
    # Then
    assert user.state == 'new_state'


def test_execute_pre_func_invalid_state():
    # Given
    config = {
        'actions': {
        }
    }
    dispatcher = Dispatcher(config)
    user = Mock(state='invalid_state')
    # When
    with pytest.raises(KeyError):
        dispatcher.execute_pre_func(user)


def test_execute_post_func_exists():
    # Given
    def func(user):
        user.state = 'new_state'
    config = {
        'actions': {
            'home': {
                'func': lambda user, text: text, 'post-func': func, }}}
    dispatcher = Dispatcher(config)
    user = Mock(state='home')
    # When
    dispatcher.execute_post_func(user)
    # Then
    assert user.state == 'new_state'


def test_execute_post_func_invalid_state():
    # Given
    config = {
        'actions': {
        }
    }
    dispatcher = Dispatcher(config)
    user = Mock(state='invalid_state')
    # When
    with pytest.raises(KeyError):
        dispatcher.execute_post_func(user)


def test_execute_func():
    # Given
    def test_func(user):
        user.state = 'new_state'
    config = {
        'actions': {
            'home': {
                'func': lambda user, text: test_func(user), }}}
    dispatcher = Dispatcher(config)
    user = Mock(state='home')
    # When
    dispatcher.execute_func(user, "som_fake_input")
    # Then
    assert user.state == 'new_state'


def test_execute_post_func_invalid_state():
    # Given
    config = {
        'actions': {
        }
    }
    dispatcher = Dispatcher(config)
    user = Mock(state='invalid_state')
    # When
    with pytest.raises(KeyError):
        dispatcher.execute_post_func(user)
