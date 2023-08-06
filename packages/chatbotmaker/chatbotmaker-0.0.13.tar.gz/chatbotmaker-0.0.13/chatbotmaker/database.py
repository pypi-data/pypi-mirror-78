""" Database class file"""
from . import Column, Integer, String, relationship, ForeignKey,\
              declarative_base, engine_from_config, sessionmaker
from . import ExtendedUser


def create_user_class(base):
    """ Creates a User class with the given relationships (rs) """
    class User(base):
        """ User class """
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        fb_id = Column(String)
        state = Column(String)
        # Arguments (One to Many)
        arguments = relationship('Argument', back_populates='user',
                                 lazy='dynamic')

        def __init__(self, fb_id, state='welcome'):
            self.fb_id = fb_id
            self.state = state
            self.extended = None

        def __getattr__(self, name):
            # gettatribute avoids recursion calling gettattr again
            if self.__getattribute__('extended') is not None:
                return getattr(self.extended, name)
            return self.__getattribute__(name)

        def extend_user(self, messenger, dispatcher, database):
            """ Add sugar calling methods """
            self.extended = ExtendedUser(self, messenger, dispatcher, database)

    return User


def create_argument_class(base):
    """ Creates a Argument class with the given relationships (rs) """
    class Argument(base):
        """ Argument class """
        __tablename__ = 'arguments'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        value = Column(String)
        # User 1-Many relationship
        user_id = Column(Integer, ForeignKey('users.id'))
        user = relationship('User', uselist=False,
                            back_populates='arguments')

        def __init__(self, name, value):
            self.name = name
            self.value = value

    return Argument


def add_relationship(class_to_add, name: str, value):
    """ Add a relationship (value) with name to class_to_add """
    setattr(class_to_add, name, value)


class Database:
    """ Database representation (only show what exists) """

    session = None

    def __init__(self, config: dict, base=None):
        self.base = declarative_base() if base is None else base
        # Create default tables
        self.user_class = create_user_class(self.base)
        self.argument_class = create_argument_class(self.base)
        # Continue database config
        self.engine = engine_from_config(config)
        self.base.metadata.create_all(self.engine)
        self.session_maker = sessionmaker()
        self.session_maker.configure(bind=self.engine)

    def create_session(self):
        self.session = self.session_maker()
        return self.session

    def close_session(self, commit=True):
        if self.session is None:
            raise Exception("Trying to close but there are no open session.")
        if commit:
            self.session.commit()
        self.session.close()
        self.session = None
