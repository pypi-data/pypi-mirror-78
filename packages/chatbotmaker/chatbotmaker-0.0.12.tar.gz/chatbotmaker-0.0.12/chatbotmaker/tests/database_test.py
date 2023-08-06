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


def test_init_not_create_database():
    with patch.object(Database, 'create_database', Mock()):
        config = {'sqlalchemy.url': 'sqlite:///foo.db'}
        database = Database(config, create_database=False)
        assert database.create_database.call_count == 0


def test_init_create_database():
    with patch.object(Database, 'create_database', Mock()):
        config = {'sqlalchemy.url': 'sqlite:///foo.db'}
        database = Database(config)
        database.create_database.assert_called_once()
    database.base = Mock()
    database.create_database()
    database.base.metadata.create_all.assert_called_once()


def test_create_relation_ship():
    name, value = 'a_name', Mock()
    user_class = Mock()
    add_relationship(user_class, name, value)
    assert user_class.__dict__.get(name) is not None


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
