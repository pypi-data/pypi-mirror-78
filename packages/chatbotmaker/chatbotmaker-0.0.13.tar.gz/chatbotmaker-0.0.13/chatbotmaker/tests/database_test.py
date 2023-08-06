from .. import database as db
from ..database import Database, create_user_class, create_argument_class,\
                       add_relationship
from .. import declarative_base, Column, Integer, relationship
from . import pytest, os, patch, Mock


@pytest.mark.parametrize('generator,name,attributes', [
    (create_user_class, 'users',
     ['id', 'fb_id', 'state', 'arguments', 'extend_user']),
    (create_argument_class, 'arguments',
     ['id', 'name', 'value', 'user_id', 'user']),
])
def test_create_orm_classes(generator, name, attributes):
    # When
    base = declarative_base()
    user_class = generator(base)
    # Then
    assert user_class.__dict__.get('__tablename__') == name
    for attribute in attributes:
        assert attribute in user_class.__dict__.keys()


def test_create_relation_ship():
    name, value = 'a_name', Mock()
    user_class = Mock()
    add_relationship(user_class, name, value)
    assert user_class.__dict__.get(name) is not None


def test_init_setup_database_connection():
    config = {'test': 'value'}
    engine = Mock()
    engine_from_cfg = Mock(return_value=engine)
    with patch.object(db, 'engine_from_config', engine_from_cfg) as engine_cfg:
        database = Database(config, Mock())
        engine_cfg.assert_called_once_with(config)
        database.base.metadata.create_all.assert_called_once_with(engine)


@patch.object(db, 'engine_from_config')
def test_init_setup_session(engine_cfg):
    session_maker = Mock()
    with patch.object(db, 'sessionmaker', Mock(return_value=session_maker)):
        database = Database({}, Mock())
        assert database.session_maker == session_maker
        database.session_maker.configure.\
            assert_called_once_with(bind=database.engine)


@patch.object(db, 'engine_from_config')
def test_create_session(engine_cfg):
    database = Database({}, Mock())
    new_sess = Mock()
    with patch.object(database, 'session_maker', Mock(return_value=new_sess)):
        assert database.create_session() == new_sess
        assert database.session == new_sess


@patch.object(db, 'engine_from_config')
def test_close_session_missing_session_open(engine_cfg):
    database = Database({}, Mock())
    new_sess = Mock()
    with patch.object(database, 'session_maker', Mock(return_value=new_sess)):
        with pytest.raises(Exception) as exception_info:
            database.close_session()
        assert 'no open session' in str(exception_info)


@patch.object(db, 'engine_from_config')
def test_close_session_with_commit(engine_cfg):
    database = Database({}, Mock())
    new_sess = Mock()
    with patch.object(database, 'session_maker', Mock(return_value=new_sess)):
        database.create_session()
        database.close_session()
    new_sess.commit.assert_called_once()
    new_sess.close.assert_called_once()
    assert database.session is None


@patch.object(db, 'engine_from_config')
def test_close_session_without_commit(engine_cfg):
    database = Database({}, Mock())
    new_sess = Mock()
    with patch.object(database, 'session_maker', Mock(return_value=new_sess)):
        database.create_session()
        database.close_session(commit=False)
    assert new_sess.commit.call_count == 0
    new_sess.close.assert_called_once()
    assert database.session is None


class Empty:
    pass


def test_create_user():
    # Given
    user_class = create_user_class(Empty)
    # When
    user = user_class('some_id', 'some_state')
    # Then
    assert user.fb_id == 'some_id'
    assert user.state == 'some_state'


def test_create_user_and_extend():
    # Given
    user_class = create_user_class(Empty)
    user = user_class('some_id', 'some_state')
    # When
    user.extend_user(Mock(), Mock(), Mock())
    # Then
    assert user.extended is not None

    # When
    user.change_state('new_state')
    # Then
    user.extended.dispatcher.execute_pre_func.assert_called_once()
    assert user.state == 'new_state'


def test_not_extended_user_missing_attr_arg_redirection():
    # Given
    user_class = create_user_class(Empty)
    user = user_class('user_id', 'some_state')
    # When / Then nothing
    with pytest.raises(AttributeError) as exception_info:
        user.attribute_not_existing
    assert "'User'" in str(exception_info)


def test_extended_user_missing_attr_arg_redirection():
    # Given
    user_class = create_user_class(Empty)
    user = user_class('user_id', 'some_state')
    user.extend_user(Mock(), Mock(), Mock())
    # When / Then nothing
    with pytest.raises(AttributeError) as exception_info:
        user.attribute_not_existing
    assert "'ExtendedUser'" in str(exception_info)


def test_create_argument():
    # Given
    argument_class = create_argument_class(Empty)
    # When
    argument = argument_class('some_name', 'some_value')
    # Then
    assert argument.name == 'some_name'
    assert argument.value == 'some_value'
