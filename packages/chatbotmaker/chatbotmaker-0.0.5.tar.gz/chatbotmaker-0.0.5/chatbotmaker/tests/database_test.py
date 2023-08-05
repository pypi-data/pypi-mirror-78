from ..database import Database, create_user_class, create_argument_class
from .. import declarative_base, Column, Integer
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


def test_init_not_create_database():
    with patch.object(Database, 'create_database', Mock()):
        config = {'sqlalchemy.url': 'sqlite:///foo.db'}
        database = Database(config, create_database=False)
        assert database.create_database.call_count == 0


def test_init_create_database():
    try:
        with patch.object(Database, 'create_database', Mock()):
            config = {'sqlalchemy.url': 'sqlite:///foo.db'}
            database = Database(config)
            database.create_database.assert_called_once()
        database.base = Mock()
        database.create_database()
        database.base.metadata.create_all.assert_called_once()
    except Exception as E:
        raise E
    finally:
        try:
            os.remove('foo.db')
        except OSError:
            pass


"""
def test_create_user():
    user = user_class('some_id', 'some_state')
    assert user.fb_id == 'some_id'
    assert user.state == 'some_state'


def test_create_user_and_extend():
    user = user_class('some_id', 'some_state')
    user.extend_user(Mock(), Mock(), Mock())
    user.change_state('new_state')
    user.extended.dispatcher.execute_pre_func.assert_called_once()
    assert user.state == 'new_state'


def test_create_argument():
    argument = argument_class('some_name', 'some_value')
    assert argument.name == 'some_name'
    assert argument.value == 'some_value'
"""
