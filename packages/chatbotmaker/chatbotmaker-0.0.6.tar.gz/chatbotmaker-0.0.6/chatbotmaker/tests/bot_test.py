from ..bot import Bot
from .. import ExtendedUser
from . import Mock, patch


def test_user_handle_query_commit_close_Database():
    # Given
    messenger, dispatcher, database = Mock(), Mock(), Mock()
    bot = Bot({}, messenger, dispatcher, database)
    database.session_maker.return_value = (session := Mock())
    # When
    bot.user_handle('user_id', 'user_message')
    # Then
    session.query.assert_called_once_with(database.user_class)
    session.commit.assert_called_once()
    session.close.assert_called_once()


def test_user_handle_extend_marks_seen_execute_handle():
    # Given
    messenger, dispatcher, database = Mock(), Mock(), Mock()
    user = Mock()
    filter_ = Mock(scalar=Mock(return_value=user))
    query = Mock(filter=Mock(return_value=filter_))
    session = Mock(query=Mock(return_value=query))
    database.session_maker = Mock(return_value=session)
    # When
    bot = Bot({}, messenger, dispatcher, database)
    bot.user_handle('user_id', 'user_message')
    # Then
    user.extend_user.assert_called_once_with(messenger, dispatcher, database)
    user.mark_seen.assert_called_once()
    user.execute_handle.assert_called_once_with('user_message')


def test_create_user_if_not_exists():
    user_id, user_message = 'user_id', 'user_message'
    # Given
    messenger, dispatcher, database = Mock(), Mock(), Mock()
    filter_ = Mock(scalar=Mock(return_value=None))
    query = Mock(filter=Mock(return_value=filter_))
    session = Mock(query=Mock(return_value=query))
    database.session_maker = Mock(return_value=session)
    # When
    bot = Bot({}, messenger, dispatcher, database)
    bot.user_handle(user_id, user_message)
    # Then
    database.user_class.assert_called_once_with(fb_id=user_id, state='welcome')
    session.add.assert_called_once()
