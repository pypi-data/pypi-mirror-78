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
    dispatcher.execute_post_func.assert_called_once_with(user.user)
    dispatcher.execute_pre_func.assert_called_once_with(user.user)
    assert user.user.state == 'welcome'


def test_init_state():
    # Given
    dispatcher = Mock()
    dispatcher.execute_pre_func = Mock()
    user = ExtendedUser(Mock(state='welcome'), None, dispatcher, None)
    # When
    user.init_state()
    # Then
    dispatcher.execute_pre_func.assert_called_once_with(user.user)


def test_mark_seen():
    # Given
    messenger = Mock()
    user = ExtendedUser(Mock(), messenger, None, None)
    # When
    user.mark_seen()
    # Then
    messenger.mark_seen.assert_called_once()


def test_execute_handle():
    # Given
    dispatcher = Mock()
    dispatcher.execute_func = Mock()
    user = ExtendedUser(None, None, dispatcher, None)
    # When
    user.execute_handle('toto')
    # Then
    dispatcher.execute_func.assert_called_once_with(user.user, 'toto')
    dispatcher.execute_enter_func.assert_called_once_with(user.user)


def test_get_argument_existing_with_default():
    # Given
    user, res = Mock(), 'result'
    user.arguments.filter().scalar().value = res
    # user.arguments.filter = Mock(scalar=Mock(return_value=mock_res))
    extended_user = ExtendedUser(user, None, None, Mock())
    # When
    arg = extended_user.get_argument('name', 'default')
    # Then
    assert arg == res


def test_get_argument_existing_no_default():
    # Given
    user, res = Mock(), 'result'
    user.arguments.filter().scalar().value = res
    # user.arguments.filter = Mock(scalar=Mock(return_value=mock_res))
    extended_user = ExtendedUser(user, None, None, Mock())
    # When
    arg = extended_user.get_argument('name')
    # Then
    assert arg == res


def test_get_argument_missing_no_default():
    # Given
    user = Mock()
    user.arguments.filter().scalar = Mock(return_value=None)
    # user.arguments.filter = Mock(scalar=Mock(return_value=mock_res))
    extended_user = ExtendedUser(user, None, None, Mock())
    # When
    arg = extended_user.get_argument('name')
    # Then
    assert arg == None


def test_get_argument_missing_with_default():
    # Given
    user = Mock()
    user.arguments.filter().scalar = Mock(return_value=None)
    # user.arguments.filter = Mock(scalar=Mock(return_value=mock_res))
    extended_user = ExtendedUser(user, None, None, Mock())
    # When
    arg = extended_user.get_argument('name', 'default')
    # Then
    assert arg == 'default'


def test_store_argument_existing():
    # Given
    user, argument = Mock(), Mock()
    user.arguments.filter().scalar = Mock(return_value=argument)
    # user.arguments.filter = Mock(scalar=Mock(return_value=mock_res))
    extended_user = ExtendedUser(user, None, None, Mock())
    # When
    extended_user.store_argument('name', 'value')
    # Then
    assert argument.value == 'value'


def test_store_argument_not_existing():
    # Given
    user, database = Mock(), Mock()
    user.arguments.filter().scalar = Mock(return_value=None)
    # user.arguments.filter = Mock(scalar=Mock(return_value=mock_res))
    extended_user = ExtendedUser(user, None, None, database)
    # When
    extended_user.store_argument('name', 'value')
    # Then
    user.arguments.append.assert_called_once()
    database.argument_class.assert_called_once_with(name='name', value='value')
