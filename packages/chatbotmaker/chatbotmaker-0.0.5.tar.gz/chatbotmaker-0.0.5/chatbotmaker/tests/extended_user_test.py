from ..extended_user import ExtendedUser
from ..database import create_user_class, create_argument_class
from . import pytest, Mock


def test_send_message():
    message, user_id = "Some message", "some_id"
    # Given
    messenger = Mock()
    messenger.mark_writing, messenger.send = Mock(), Mock()
    user = ExtendedUser(Mock(fb_id=user_id), messenger, None, None)
    # When
    user.send_message(message)
    # Then
    messenger.send.assert_called_once_with(user_id, message)
    assert messenger.mark_writing.call_count == 2
    assert ((user_id, True),) == messenger.mark_writing.call_args_list[0]
    assert ((user_id, False),) == messenger.mark_writing.call_args_list[1]


def test_change_state():
    # Given
    dispatcher = Mock()
    dispatcher.execute_pre_func, dispatcher.execute_post_func = Mock(), Mock()
    user = ExtendedUser(Mock(state='home'), None, dispatcher, None)
    # When
    user.change_state('welcome')
    # Then
    dispatcher.execute_pre_func.assert_called_once_with(user.user)
    dispatcher.execute_post_func.assert_called_once_with(user.user)
    assert user.user.state == 'welcome'


def test_execute_handle():
    # Given
    dispatcher = Mock()
    dispatcher.execute_func = Mock()
    user = ExtendedUser(None, None, dispatcher, None)
    # When
    user.execute_handle('toto')
    # Then
    dispatcher.execute_func.assert_called_once_with(user.user, 'toto')


def test_get_argument_existing_with_default():
    # Given
    # When
    # Then
    pass


def test_get_argument_existing_no_default():
    pass


def test_get_argument_missing_no_default():
    pass


def test_get_argument_missing_with_default():
    pass


def test_store_argument_existing():
    pass


def test_store_argument_not_existing():
    pass
